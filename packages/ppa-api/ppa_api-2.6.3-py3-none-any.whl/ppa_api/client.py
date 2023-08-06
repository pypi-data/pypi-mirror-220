import time
import requests
import datetime

from typing import List, Optional, Union, Callable

import timeout_decorator

from . import create, exceptions
from ._client import (
    API,
    user_query_params,
    validate_uuid,
    validate_payload,
    OptionalDict,
    minimum_version,
)
from .models import Image, Task, DelayedTask, User, Role, Group, TaskResult


class PPAClient:
    def __init__(
        self,
        address: str,
        *,
        api_key: str,
        verify: Optional[Union[bool, str]] = True,
        proxy: Optional[str] = None,
    ) -> None:
        self.address = address
        self.api_key = api_key
        self.verify = verify
        self.proxy = {"https": proxy} if proxy else None
        self.session = requests.Session()
        self.session.headers.update(
            {"Accept": "application/json", "Authorization": f"Bearer {api_key}"}
        )

        # Doing this on instantiation also checks the credentials for us.
        try:
            self.version = self._request(API.base, endpoint="version")["appliance"]
        except exceptions.NotFound:
            # Any PPA older than 2.7.1 won't have the version endpoint.
            raise exceptions.VersionError(
                "This package does not support PPA appliances older than v2.7.1."
            )

    def _request(self, api_method: Callable, **kwargs):
        return api_method(
            session=self.session,
            address=self.address,
            verify=self.verify,
            proxy=self.proxy,
            **kwargs,
        )

    @create.images
    def images(self, latest: Optional[bool] = False) -> List[Image]:
        return self._request(API.images if latest else API.revisions)

    @create.images
    def image_by_name(self, name: str) -> Optional[Image]:
        try:
            return self._request(API.images, params={"name": f"eq.{name}"})[0]
        except IndexError:
            return None

    @create.images
    def images_by_name(self, name: str) -> List[Image]:
        return self._request(API.revisions, params={"name": f"eq.{name}"})

    @create.images
    def image_by_id(self, image_id: int) -> Optional[Image]:
        try:
            return self._request(API.revisions, params={"id": f"eq.{image_id}"})[0]
        except IndexError:
            return None

    @create.tasks
    def tasks(self, deployed: Optional[bool] = None) -> List[Task]:
        return self._request(
            API.tasks,
            params={}
            if deployed is None
            else {"deployed": f"eq.{'true' if deployed is True else 'false'}"},
        )

    @create.tasks
    def tasks_by_name(self, name: str, days: Optional[bool] = None) -> List[Task]:
        params = {"image": f"eq.{name}", "order": "started_at.desc"}
        if days is not None:
            params.update(
                started_at=(
                    f"gt.{(datetime.datetime.utcnow() - datetime.timedelta(days=days)).strftime('%Y-%m-%dT%H:%M')}"
                )
            )
        return self._request(API.tasks, params=params)

    @create.tasks
    def recent_tasks(self, days: Optional[int] = 30):
        return self._request(
            API.tasks,
            params={
                "order": "started_at.desc",
                "started_at": (
                    f"gt.{(datetime.datetime.utcnow() - datetime.timedelta(days=days)).strftime('%Y-%m-%dT%H:%M')}"
                ),
            },
        )

    @minimum_version("2.8.0")
    @create.delayed_tasks
    def delayed_tasks(self) -> List[DelayedTask]:
        return self._request(API.delayed_tasks)

    @minimum_version("2.8.0")
    @create.delayed_tasks
    def delayed_task_by_id(self, delayed_task_id: int) -> Optional[DelayedTask]:
        try:
            return self._request(API.delayed_tasks, params={"id": f"eq.{delayed_task_id}"})[0]
        except IndexError:
            return None

    @minimum_version("2.8.0")
    @create.delayed_tasks
    def tasks_delayed_by_me(self) -> List[Task]:
        return self._request(API.delayed_tasks, params={"is_owner": "eq.true"})

    @minimum_version("2.8.0")
    @create.delayed_tasks
    def pending_delayed_tasks(self) -> List[Task]:
        return self._request(API.delayed_tasks, params={"is_pending": "eq.true"})

    @minimum_version("2.8.0")
    @create.delayed_tasks
    def processed_delayed_tasks(self) -> List[Task]:
        return self._request(API.delayed_tasks, params={"is_pending": "eq.false"})

    @create.tasks
    def task_by_uuid(self, uuid: str) -> Optional[Task]:
        try:
            return self._request(API.tasks, params={"uuid": f"eq.{validate_uuid(uuid)}"})[0]
        except IndexError:
            return None

    @create.tasks
    def tasks_started_by_me(self) -> List[Task]:
        return self._request(API.tasks, params={"is_owner": "eq.true"})

    @create.users
    def users(self) -> List[User]:
        return self._request(
            API.users,
            params={"select": user_query_params, "deleted_at": "is.null"},
        )

    @create.users
    def licensed_users(self) -> List[User]:
        return self._request(
            API.users,
            params={"select": user_query_params, "deleted_at": "is.null", "active": "eq.true"},
        )

    @create.users
    def deleted_users(self) -> List[User]:
        return self._request(
            API.users,
            params={"select": user_query_params, "deleted_at": "not.is.null"},
        )

    @create.users
    def user_by_id(self, user_id: Union[str, int]) -> Optional[User]:
        try:
            return self._request(
                API.users,
                params={"id": f"eq.{user_id}", "select": user_query_params},
            )[0]
        except IndexError:
            return None

    @create.users
    def user_by_username(self, name: str) -> Optional[User]:
        try:
            return self._request(
                API.users,
                params={"username": f"ilike.*\\{name}", "select": user_query_params},
            )[0]
        except IndexError:
            return None

    @create.roles
    @minimum_version("2.10.0")
    def roles(self) -> List[Role]:
        return self._request(API.roles)

    @create.roles
    @minimum_version("2.10.0")
    def role_by_name(self, name: str) -> Role:
        try:
            return self._request(API.roles, params={"name": f"ilike.*\\{name}"})[0]
        except IndexError:
            return None

    @create.roles
    @minimum_version("2.10.0")
    def role_by_id(self, role_id: Union[str, int]) -> Group:
        try:
            return self._request(API.roles, params={"id": f"eq.{role_id}"})[0]
        except IndexError:
            return None

    @create.groups
    @minimum_version("2.10.0")
    def groups(self) -> List[Group]:
        return self._request(API.groups)

    @create.groups
    @minimum_version("2.10.0")
    def group_by_id(self, group_id: Union[str, int]) -> Group:
        try:
            return self._request(API.groups, params={"id": f"eq.{group_id}"})[0]
        except IndexError:
            return None

    @create.groups
    @minimum_version("2.10.0")
    def group_by_name(self, name: str) -> Group:
        try:
            return self._request(API.groups, params={"name": f"ilike.*\\{name}"})[0]
        except IndexError:
            return None

    def task_running(self, uuid: str) -> bool:
        uuid = validate_uuid(uuid)
        if task := self.task_by_uuid(uuid):
            return task.is_running
        raise exceptions.NoTaskFound(f"No task was found with UUID '{uuid}'.")

    def wait_for_task(
        self,
        uuid: str,
        timeout: Optional[int] = 600,
        interval: Optional[Union[int, float]] = 5,
    ) -> Task:
        @timeout_decorator.timeout(
            timeout,
            timeout_exception=exceptions.WaitTimeout,
            exception_message=f"Task has not finished after {timeout} seconds.",
        )
        def _execute():
            while self.task_running(uuid):
                time.sleep(interval)
            return self.task_by_uuid(uuid)

        return _execute()

    def start_task_async(self, name: str, *, payload: OptionalDict = None) -> Task:
        if not self.image_by_name(name):
            raise exceptions.NoImageFound(
                f"There are no images delegated to your identity with the name '{name}'."
            )
        try:
            return self.task_by_uuid(
                self._request(
                    API.rpc,
                    endpoint="start_task",
                    data={"image_name": name, "payload": payload},
                )
            )
        except exceptions.RequestError as e:
            if "must be deployed" in str(e):
                raise exceptions.ImageNotDeployed(
                    f"The task cannot be started as image '{name}' is not deployed."
                )
            raise e

    def start_task(
        self,
        name: str,
        *,
        payload: OptionalDict = None,
        timeout: Optional[int] = 600,
        interval: Optional[int] = 5,
    ) -> Task:
        return self.wait_for_task(
            self.start_task_async(name, payload=validate_payload(payload)).uuid,
            timeout=timeout,
            interval=interval,
        )

    @minimum_version("2.8.0")
    def delay_task(
        self,
        name: str,
        *,
        delay: int,
        description: str,
        payload: OptionalDict = None,
    ) -> DelayedTask:
        if not self.image_by_name(name):
            raise exceptions.NoImageFound(
                f"There are no images delegated to your identity with the name '{name}'."
            )
        try:
            return self.delayed_task_by_id(
                self._request(
                    API.rpc,
                    endpoint="delay_task",
                    data={
                        "image_name": name,
                        "payload": payload,
                        "description": description,
                        "delay": delay,
                    },
                )
            )
        except exceptions.RequestError as e:
            if "no deployed version found" in str(e).lower():
                raise exceptions.ImageNotDeployed(
                    f"The delayed task cannot be created as image '{name}' is not deployed."
                )
            raise e

    def cancel_task(
        self,
        uuid: str,
    ) -> None:
        uuid = validate_uuid(uuid)
        try:
            self._request(API.rpc, endpoint="cancel_task", data={"uuid": validate_uuid(uuid)})
        except exceptions.NotFound:
            raise exceptions.NoTaskFound(
                f"Task with UUID '{uuid}' is either not running or does not exist."
            )

    def task_succeeded(self, uuid: str) -> bool:
        exit_code = self.task_by_uuid(uuid).exit_code
        if exit_code is None:
            raise exceptions.TaskStillRunning(f"Task with UUID '{uuid}' is still running.")
        return exit_code == 0

    @create.task_result
    def get_task_result(self, uuid: str) -> TaskResult:
        if task_result := self._request(
            API.rpc, endpoint="task_result", data={"uuid": validate_uuid(uuid)}
        ):
            return task_result
        raise exceptions.NoData(f"No result data was saved by task with UUID '{uuid}'.")

    def set_kerberos_config(
        self,
        address: str,
        domain: str,
        username: str,
        password: str,
        enabled: Optional[bool] = True,
    ) -> None:
        try:
            self._request(
                API.config,
                data={
                    "key": "kerberos",
                    "value": {
                        "host": address,
                        "realm": domain,
                        "username": username,
                        "secret": password,
                        "enabled": enabled,
                        "config": "",
                    },
                },
            )
        except exceptions.RequestError as e:
            if all((e.message is not None, e.message.lower() == "invalid kerberos configuration")):
                raise exceptions.ConfigurationError(f"{e.message}, {e.error}")
            raise e
        except exceptions.ServerError as e:
            if "cannot unmarshal" in str(e):
                raise exceptions.ConfigurationError(
                    "Invalid Kerberos Configuration. One or more of the supplied values is not in the correct format."
                )
            raise e
