import json
import logging
import functools

from uuid import UUID
from distutils.version import StrictVersion
from typing import Optional, Dict, Any, List, Union, Callable

import requests

from requests.compat import urljoin  # type: ignore
from requests.utils import prepend_scheme_if_needed

from . import exceptions


logger = logging.getLogger(__name__)

user_query_params = (
    "id,username,name,email,authenticated_at,active,deleted_at,groups,permissions,roles_count"
)

OptionalDict = Optional[Dict[str, Any]]
AnyJson = Union[None, bool, int, float, str, List[Any], Dict[str, Any]]


def validate_uuid(uuid: str) -> str:
    try:
        UUID(uuid, version=4)
        return uuid
    except ValueError:
        raise exceptions.ParameterError("The format of the supplied UUID is invalid.")


def validate_payload(payload: AnyJson) -> AnyJson:
    try:
        json.dumps(payload)
    except TypeError:
        raise exceptions.ParameterError("The supplied payload cannot be converted to JSON.")
    return payload


def minimum_version(minimum_version: str):
    def _function_wrapper(method):
        def _check_version(instance, *args, **kwargs):
            if StrictVersion(minimum_version) > StrictVersion(instance.version):
                raise exceptions.VersionError(
                    f"The {method.__name__} method requires PPA version {minimum_version} or later, but your version is {instance.version}."
                )
            return method(instance, *args, **kwargs)

        return _check_version

    return _function_wrapper


def api_call(func) -> Callable:
    @functools.wraps(func)
    def _execute(*, address: str, api: str, endpoint: str, **kwargs: Any) -> AnyJson:
        response = func(address=address, api=api, endpoint=endpoint, **kwargs)
        try:
            response_json = response.json()
        except json.decoder.JSONDecodeError:
            if response.status_code in {
                204,  # The request was processed but no data was returned
                201,  # Resource created successfully
            }:
                return None
            elif response.status_code == 403:
                raise exceptions.AuthenticationFailed(
                    "Forbidden (403). Failed to authenticate to PPA using the supplied API key."
                )
            elif response.status_code == 404:
                raise exceptions.NotFound(
                    f"Not Found (404). The {endpoint} endpoint does not exist."
                )
            raise exceptions.InvalidResponse(
                f"Unhandled Non-JSON Response ({response.status_code}). Response body: {response.text}."
            )

        if response.status_code == 200:
            return response_json

        exception_kwargs = {
            "address": address,
            "api": api,
            "endpoint": endpoint,
            "status_code": response.status_code,
            "response_json": response_json,
        }
        try:
            raise exceptions.EXCEPTION_MAP[response.status_code](**exception_kwargs)
        except KeyError:
            raise exceptions.UnhandledRequestError(
                f"Unhandled ({response.status_code}). Response body: {response_json}."
            )

    return _execute


@api_call
def _get_request(
    *,
    session: requests.Session,
    address: str,
    api: Optional[str],
    endpoint: str,
    proxy: Optional[str],
    verify: Union[bool, str],
    params: OptionalDict = None,
):
    return session.get(
        urljoin(
            prepend_scheme_if_needed(address, "https"),
            f"/backend/v1/{api}/{endpoint}" if api else f"/backend/v1/{endpoint}",
        ),
        params=params,
        verify=verify,
        proxies=proxy,
    )


@api_call
def _post_request(
    *,
    session: requests.Session,
    address: str,
    api: str,
    endpoint: str,
    proxy: Optional[str],
    verify: Union[bool, str],
    data: OptionalDict = None,
):
    return session.post(
        urljoin(
            prepend_scheme_if_needed(address, "https"),
            f"/backend/v1/{api}/{endpoint}" if api else f"/backend/v1/{endpoint}",
        ),
        json=data,
        verify=verify,
        proxies=proxy,
    )


@api_call
def _patch_request(
    *,
    session: requests.Session,
    address: str,
    api: str,
    endpoint: str,
    params: Optional[dict] = None,
    proxy: Optional[str],
    verify: Union[bool, str],
    data: OptionalDict = None,
):
    return session.patch(
        urljoin(
            prepend_scheme_if_needed(address, "https"),
            f"/backend/v1/{api}/{endpoint}" if api else f"/backend/v1/{endpoint}",
        ),
        params=params,
        json=data,
        verify=verify,
        proxies=proxy,
    )


class API:
    base = functools.partial(_get_request, api=None)
    tasks = functools.partial(_get_request, api="rest", endpoint="tasks")
    delayed_tasks = functools.partial(_get_request, api="rest", endpoint="delayed_tasks")
    users = functools.partial(_get_request, api="rest", endpoint="users")
    roles = functools.partial(_get_request, api="rest", endpoint="roles")
    groups = functools.partial(_get_request, api="rest", endpoint="groups")
    images = functools.partial(_get_request, api="rest", endpoint="images")
    revisions = functools.partial(_get_request, api="rest", endpoint="revisions")
    rpc = functools.partial(_post_request, api="rest/rpc")
    config = functools.partial(_post_request, api="rest", endpoint="config")
