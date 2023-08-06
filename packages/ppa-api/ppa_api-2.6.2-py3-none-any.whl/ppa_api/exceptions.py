import json

from typing import Optional, Dict, Any

from requests.compat import urljoin  # type: ignore
from requests.utils import prepend_scheme_if_needed


class RequestError(Exception):
    def __init__(
        self,
        *,
        address: str,
        api: Optional[str] = None,
        endpoint: str,
        status_code: int,
        response_json: Dict[str, Any],
    ):
        self.address = urljoin(
            prepend_scheme_if_needed(address, "https"),
            f"/backend/v1/{api}/{endpoint}" if api else f"/backend/v1/{endpoint}",
        )
        self.status_code = status_code
        self.response_json = response_json

        # Response JSON usually looks like this:
        #
        # {
        #   'hint': 'application/json; charset=utf-8',
        #   'details': '{"message":"Invalid Kerberos configuration", "error": {"secret":["Invalid password"]}}'
        # }
        #
        # The 'details' key is a string so it needs to be JSON-loaded.

        self.details, self.message, self.error = None, None, None  # Defaults
        if details := self.response_json.get("details"):
            try:
                self.details = json.loads(details)
                # Setting these makes it easier to catch specific errors in the client methods.
                if isinstance(self.details, dict):
                    self.message, self.error = [self.details.get(k) for k in ["message", "error"]]
                else:
                    # Unexpected format, leave error & message as None.
                    pass
            except json.JSONDecodeError:
                # The details key is not JSON, take the raw string & leave error & message as None.
                self.details = details
            exception_message = (
                f"({self.status_code}) Request to {self.address} failed: {self.details}"
            )
        else:
            exception_message = (
                f"({self.status_code}) Request to {self.address} failed: {self.response_json}"
            )
        super().__init__(exception_message)


class ParameterError(Exception):
    pass


class ConfigurationError(Exception):
    pass


class ServerError(Exception):
    pass


class InvalidResponse(Exception):
    pass


class PermissionDenied(Exception):
    pass


class NoTaskFound(Exception):
    pass


class NoImageFound(Exception):
    pass


class ImageNotDeployed(Exception):
    pass


class WaitTimeout(Exception):
    pass


class TaskStillRunning(Exception):
    pass


class AuthenticationFailed(Exception):
    pass


class CreditsRequired(Exception):
    pass


class UnhandledRequestError(Exception):
    pass


class NotFound(Exception):
    pass


class NoData(Exception):
    pass


class VersionError(Exception):
    pass


def _format_exception_string(json):
    return list(
        map(lambda key: json.get(key, f"no {key} provided"), ["message", "details", "hint"])
    )


EXCEPTION_MAP = {
    400: lambda **kwargs: RequestError(**kwargs),
    402: lambda **kwargs: CreditsRequired(
        "Credits Required (402). Cannot start the task as there are 0 credits available."
    ),
    403: lambda **kwargs: PermissionDenied(
        "Forbidden (403). The user associated with the API key does "
        f"not have the required {kwargs['endpoint']} permissions."
    ),
    404: lambda **kwargs: NotFound(
        "Not Found (404). Either the endpoint or supplied record does not exist."
    ),
    500: lambda **kwargs: ServerError(
        "Internal Server Error (500). Message: {}. Details: {}. Hint: {}.".format(
            *_format_exception_string(kwargs["response_json"])
        )
    ),
}
