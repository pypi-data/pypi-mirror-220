import asyncio
import functools
import inspect
import json
import traceback
from typing import *  # type: ignore
from . import errors
from .errors import RPCError

import uniserde
from uniserde.case_convert import all_lower_to_camel_case
from uniserde import Jsonable


__all__ = [
    "Unicall",
    "local",
    "remote",
    "RPCError",
    "errors",
    "Jsonable",
]


def _parse_method(
    method: Callable[..., Any],
    name: Optional[str],
    parameter_names,
) -> Tuple[str, List[Tuple[str, Type]], Optional[Type]]:
    # Make sure the method is callable and awaitable
    if not callable(method):
        raise TypeError(f"Expected a method, not {type(method)}")

    if not inspect.iscoroutinefunction(method):
        raise TypeError(
            f"Expected an async method. Did you forget `async` before `{method.__name__}`?"
        )

    # Make sure the function has a return type annotation. None is also okay
    if "return" not in method.__annotations__:
        raise ValueError(
            f"The method `{method.__name__}` is missing a return type annotation. Did you forget a `-> None`?",
        )

    # Get the method name
    if name is None:
        if not method.__name__.islower():
            raise ValueError(
                f"The method `{method.__name__}` should be all lower case. If you don't want for unicall to change the name, explicitly pass a `name=...` parameter",
            )

        name = all_lower_to_camel_case(method.__name__)

    # Get the parameters, taking care to strip `self`
    signature_parameters = list(inspect.signature(method).parameters.values())[1:]

    if isinstance(parameter_names, str):
        if parameter_names == "camelCase":
            parameter_names = []

            for param in signature_parameters:
                if not param.name.islower():
                    raise ValueError(
                        f"The parameter `{param.name}` should be all lower case. If you don't want for unicall to change the name, explicitly pass a `parameter_names=...` parameter",
                    )

                parameter_names.append(all_lower_to_camel_case(param.name))

        elif parameter_names == "keep":
            parameter_names = [param.name for param in signature_parameters]

        else:
            raise ValueError(
                f"`parameter_names` needs to either be a string, or list of strings, not `{parameter_names}`"
            )

    # Make sure the number of parameter names matches the number of
    # parameters
    if len(parameter_names) != len(signature_parameters):
        raise ValueError(
            f"Expected {len(signature_parameters)} parameter name(s), but got {len(parameter_names)}",
        )

    # Get the parameter types and store them
    parameters = []

    for param_name, param in zip(parameter_names, signature_parameters):
        # Make sure the parameter is annotated
        if param.annotation is param.empty:
            raise ValueError(
                f"The parameter `{param.name}` is missing a type annotation",
            )

        parameters.append((param_name, param.annotation))

    return name, parameters, inspect.signature(method).return_annotation


def _wrap_remote_method(
    method: Callable,
    name: Optional[str],
    parameter_names: Literal["camelCase", "keep"] | List[str] = "camelCase",
):
    signature = inspect.signature(method)

    name, formal_parameters, return_type = _parse_method(
        method,
        name,
        parameter_names,
    )

    async def wrapper(self, *args: Any, **kwargs: Any) -> Any:
        assert isinstance(self, Unicall), self

        # Bind the arguments, taking care to drop `self`
        bound_args = signature.bind(self, *args, **kwargs)
        bound_args.apply_defaults()
        bound_args.arguments.pop("self")
        passed_parameters = bound_args.arguments.values()

        # Serialize the arguments
        serialized_args = {}

        for (param_name_json, param_type), param_value_python in zip(
            formal_parameters, passed_parameters
        ):
            serialized_args[param_name_json] = uniserde.as_json(
                param_value_python,
                as_type=param_type,
            )

        # Call the method
        result_serialized = await self.call_json(
            name,
            serialized_args,
            # Functions may throw errors. Because of this, make sure to always
            # wait for the response, regardless of whether the method is
            # annotated with as returning `None`.
            await_response=True,
        )

        # Deserialize the result
        if return_type is None:
            return None

        try:
            return uniserde.from_json(result_serialized, return_type)
        except uniserde.SerdeError as err:
            raise RPCError(
                f"Invalid server response. Expected a value of type `{return_type.__name__}`, but got `{result_serialized}`",
                error_code=errors.JSONRPC_SERVER_ERROR,
                debug_object=(result_serialized, return_type, err),
            ) from None

    return functools.wraps(method)(wrapper)


@overload
def local(method: Callable[..., Any]):
    ...


@overload
def local(
    name: Optional[str] = None,
    *,
    parameter_names: Literal["camelCase", "keep"] | List[str] = "camelCase",
):
    ...


def local(*args, **kwargs):
    """
    Decorator version of `add_local_route`.
    """

    # If called with a single method argument, register it
    if len(args) == 1 and not kwargs and callable(args[0]):
        method = args[0]
        method._unicall_local_ = {
            "name": None,
            "parameter_names": "camelCase",
        }

        return method

    # Otherwise, return a decorator
    def build_decorator(
        name: Optional[str] = None,
        *,
        parameter_names: Literal["camelCase", "keep"] | List[str] = "camelCase",
    ):
        def decorator(method: Callable[..., Any]):
            method._unicall_local_ = {
                "name": name,
                "parameter_names": parameter_names,
            }
            return method

        return decorator

    return build_decorator(*args, **kwargs)


@overload
def remote(method: Callable):
    ...


@overload
def remote(
    name: Optional[str] = None,
    *,
    parameter_names: Literal["camelCase", "keep"] | List[str] = "camelCase",
):
    ...


def remote(*args, **kwargs):
    """
    Registers a remote method, so it can be called locally.
    """

    # If called with a single method argument, register it
    if len(args) == 1 and not kwargs and callable(args[0]):
        return _wrap_remote_method(args[0], None)

    # Otherwise, return a decorator
    def build_decorator(
        name: Optional[str] = None,
        *,
        parameter_names: Literal["camelCase", "keep"] | List[str] = "camelCase",
    ):
        def decorator(method: Callable):
            return _wrap_remote_method(
                method,
                name,
                parameter_names=parameter_names,
            )

        return decorator

    return build_decorator(*args, **kwargs)


class Unicall:
    # Maps (JSON) method names to (method, parameters, return type) tuples. The
    # parameters themselves are tuples [name, type].
    #
    # This value must be separate for each class. Thus, it is never actually
    # initialized here, but rather by `add_local_route`.
    _local_methods_: Dict[str, Tuple[Callable, List[Tuple[str, Type]], Type]]

    def __init__(
        self,
        *,
        send_message: Callable[[Jsonable], Awaitable[None]],
        errors: Literal["raise", "swallow", "print"] = "raise",
    ):
        self._send_message = send_message
        self._errors = errors

        self._next_free_remote_id = 0
        self._in_flight_requests: Dict[int | str, asyncio.Future[Any]] = {}

    def __init_subclass__(cls) -> None:
        # Make sure the class has a `_local_methods_` attribute set locally.
        # Inherited ones don't count.
        assert not hasattr(cls, "_local_methods_")
        cls._local_methods_ = {}

        # Find all methods annotated with @local and register them
        for member in vars(cls).values():
            try:
                args = member._unicall_local_
            except AttributeError:
                continue

            assert callable(member), member
            cls.add_local_route(member, **args)

    @classmethod
    def add_local_route(
        cls,
        method: Callable[..., Any],
        name: Optional[str] = None,
        *,
        parameter_names: Literal["camelCase", "keep"] | List[str] = "camelCase",
    ):
        """
        Registers the method, allowing remote clients to call it.
        """

        # Parse the method. This also verifies the passed parameters.
        name, parameters, return_type = _parse_method(
            method,
            name=name,
            parameter_names=parameter_names,
        )

        # Store the method
        cls._local_methods_[name] = (
            method,
            parameters,
            return_type,
        )

    async def handle_message(self, message: Union[str, bytes, Jsonable]) -> None:
        # Move the code to a helper function, so exceptions can easily be
        # handled in one place.
        try:
            await self._handle_message_inner(message)
        except RPCError:
            if self._errors == "raise":
                raise

            if self._errors == "print":
                traceback.print_exc()

            return None

    async def _handle_message_inner(
        self,
        message: Union[str, bytes, Jsonable],
    ) -> None:
        # TODO: Honor the `errors` parameter

        # Bytes?
        if isinstance(message, bytes):
            try:
                message = message.decode("utf-8")
            except UnicodeDecodeError as err:
                raise RPCError(
                    f"The message is not valid UTF-8: {err}",
                    error_code=errors.JSONRPC_PARSE_ERROR,
                    debug_object=message,
                )

        # String?
        if isinstance(message, str):
            try:
                message = json.loads(message)
            except json.JSONDecodeError as err:
                raise RPCError(
                    f"The message is not valid JSON: {err}",
                    error_code=errors.JSONRPC_PARSE_ERROR,
                    debug_object=message,
                )

        # Make sure this is a dict
        if not isinstance(message, dict):
            raise RPCError(
                f"Messages must be JSON objects, not {type(message)}",
                error_code=errors.JSONRPC_INVALID_REQUEST,
                debug_object=message,
            )

        # Is this a response, or a request?
        if "method" in message:
            await self._handle_request(message)
        else:
            await self._handle_response(message)

    async def _handle_response(self, message: Dict[str, Jsonable]) -> None:
        # Pass the message to the appropriate future
        try:
            id = message["id"]
        except KeyError:
            raise RPCError(
                f"Message is missing the `id` field",
                error_code=errors.JSONRPC_INVALID_REQUEST,
                debug_object=message,
            ) from None

        if not isinstance(id, (str, int)):
            raise RPCError(
                f"The `id` field must be a string or integer, not {type(id)}",
                error_code=errors.JSONRPC_INVALID_REQUEST,
                debug_object=message,
            )

        try:
            future = self._in_flight_requests[id]
        except KeyError:
            raise RPCError(
                f"Received a response to an unknown request with id `{id}`",
                error_code=errors.JSONRPC_INVALID_REQUEST,
                debug_object=message,
            ) from None

        # Resolve the future
        future.set_result(message)

    async def _handle_request(self, message: Dict[str, Jsonable]) -> None:
        # Parse the message
        try:
            version = message["jsonrpc"]
            method_name_json = message["method"]
            passed_parameters = message["params"]
            id = message.get("id")
        except KeyError as err:
            raise RPCError(
                f"The message is missing the `{err.args[0]}` field",
                error_code=errors.JSONRPC_INVALID_REQUEST,
                debug_object=message,
            )

        # Make sure the version is compatible
        if version != "2.0":
            raise RPCError(
                f"Unsupported JSON-RPC version: {version}",
                error_code=errors.JSONRPC_INVALID_REQUEST,
                debug_object=message,
            )

        # Verify the types of remaining fields
        if not isinstance(method_name_json, str):
            raise RPCError(
                f"The `method` field must be a string, not {type(method_name_json)}",
                error_code=errors.JSONRPC_INVALID_REQUEST,
                debug_object=message,
            )

        if not isinstance(passed_parameters, (list, dict)):
            raise RPCError(
                f"The `params` field must be a JSON object, not {type(passed_parameters)}",
                error_code=errors.JSONRPC_INVALID_REQUEST,
                debug_object=message,
            )

        if id is not None and not isinstance(id, (str, int)):
            raise RPCError(
                f"The `id` field must be ais  string or integer, not {type(id)}",
                error_code=errors.JSONRPC_INVALID_REQUEST,
                debug_object=message,
            )

        # Find the requested method
        try:
            method, formal_parameters, return_type = self._local_methods_[
                method_name_json
            ]
        except KeyError:
            raise RPCError(
                f"Unknown method: `{method_name_json}`",
                error_code=errors.JSONRPC_METHOD_NOT_FOUND,
                debug_object=message,
            ) from None

        # Deserialize the parameters
        parsed_parameters = self._deserialize_parameters(
            method_name_json,
            formal_parameters,
            passed_parameters,
        )

        # Call the method, and await it if necessary
        try:
            result = method(self, *parsed_parameters)

            if inspect.isawaitable(result):
                result = await result

        except RPCError as err:
            await self._send_message(
                {
                    "jsonrpc": "2.0",
                    "id": message.get("id"),
                    "error": {
                        "code": errors.JSONRPC_SERVER_ERROR
                        if err.error_code is None
                        else err.error_code,
                        "message": err.message,
                    },
                }
            )
            return

        except Exception as err:
            await self._send_message(
                {
                    "jsonrpc": "2.0",
                    "id": message.get("id"),
                    "error": {
                        "code": errors.JSONRPC_SERVER_ERROR,
                        "message": f"Internal server error",
                    },
                }
            )
            return

        # Skip encoding the result if it's not requested
        if id is None:
            return

        # Encode the result
        if return_type is None:
            result = None
        else:
            try:
                result = uniserde.as_json(result, as_type=return_type)
            except uniserde.SerdeError as err:
                raise RPCError(
                    f"Internal server error",
                    error_code=errors.JSONRPC_SERVER_ERROR,
                    debug_object=(result, return_type, err),
                ) from None

        # Respond
        await self._send_message(
            {
                "jsonrpc": "2.0",
                "result": result,
                "id": id,
            }
        )

    def _deserialize_parameters(
        self,
        method_name_json: str,
        formal_parameters: List[Tuple[str, Type]],
        passed_parameters: Union[List[Jsonable], Dict[str, Jsonable]],
    ) -> Iterable[Any]:
        """
        Deserialize the parameters for the given method using `uniserde`. The
        result is an iterable of the passed parameters in the order they appear
        in the method signature.

        If any parameters are missing, cannot be parsed, or are superfluous, a
        `RPCError` is raised.

        WARNING: `params` may be modified in-place.
        """

        # Turn the parameters info a flat list
        if isinstance(passed_parameters, list):
            if len(passed_parameters) != len(formal_parameters):
                raise RPCError(
                    f"Method `{method_name_json}` expects {len(formal_parameters)} parameter(s), but received {len(passed_parameters)}",
                    error_code=errors.JSONRPC_INVALID_PARAMS,
                    debug_object=passed_parameters,
                )

            passed_parameters_flat = passed_parameters

        else:
            assert isinstance(passed_parameters, dict), passed_parameters
            passed_parameters_flat = []

            for param_name_json, param_type in formal_parameters:
                try:
                    param_serialized = passed_parameters.pop(param_name_json)
                except KeyError:
                    raise RPCError(
                        f"Method `{method_name_json}` is missing parameter `{param_name_json}`",
                        error_code=errors.JSONRPC_INVALID_PARAMS,
                        debug_object=passed_parameters,
                    ) from None

                passed_parameters_flat.append(param_serialized)

            # Make sure there are no superfluous parameters
            if passed_parameters:
                raise RPCError(
                    f"Method `{method_name_json}` has received superfluous parameters: {', '.join(passed_parameters.keys())}",
                    error_code=errors.JSONRPC_INVALID_PARAMS,
                    debug_object=passed_parameters,
                ) from None

        # Deserialize them
        result = []

        for param_serialized, (param_name_json, param_type) in zip(
            passed_parameters_flat, formal_parameters
        ):
            try:
                result.append(uniserde.from_json(param_serialized, param_type))
            except uniserde.SerdeError as err:
                raise RPCError(
                    f"Invalid value for parameter `{param_name_json}` of method `{method_name_json}`: {err}",
                    error_code=errors.JSONRPC_INVALID_PARAMS,
                    debug_object=passed_parameters,
                ) from None

        return passed_parameters_flat

    async def call_json(
        self,
        method: str,
        params: Dict[str, Jsonable] = {},
        *,
        id: int | str | None = None,
        await_response: bool = True,
    ) -> Jsonable:
        # Prepare the message
        message = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": None,
        }

        # If no resposne is requested, send the message and return
        if not await_response:
            await self._send_message(message)
            return None

        # Create a unique id, and make sure other automatically generated ids
        # won't clash
        if id is None:
            id = self._next_free_remote_id
            self._next_free_remote_id += 1
        elif isinstance(id, int):
            self._next_free_remote_id = max(self._next_free_remote_id, id + 1)

        message["id"] = id

        # Register a future for the result
        future = asyncio.get_running_loop().create_future()
        self._in_flight_requests[id] = future

        try:
            # Send the message
            await self._send_message(message)

            # Wait for the result
            response = await future

        # Make sure the future is removed from the in-flight list
        finally:
            del self._in_flight_requests[id]

        # The result is a dictionary. This is ensured in `handle_message`
        assert isinstance(response, dict), response

        # Return the result, if the call was successful
        try:
            return response["result"]
        except KeyError:
            pass

        # Error?
        if "error" in response:
            try:
                error = response["error"]
                message = error["message"]
                code = error.get("code")

            except KeyError as err:
                raise RPCError(
                    f"Server response is missing the `{err.args[0]}` field",
                    error_code=errors.JSONRPC_SERVER_ERROR,
                    debug_object=response,
                ) from None

            else:
                raise RPCError(
                    message,
                    error_code=code,
                    error_data=error.get("data"),
                    debug_object=response,
                )

        # Invalid response
        raise RPCError(
            f"Server response has neither a `result` nor `error` field",
            error_code=errors.JSONRPC_INVALID_REQUEST,
            debug_object=response,
        )
