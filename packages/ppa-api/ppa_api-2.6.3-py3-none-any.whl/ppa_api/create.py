import re
import functools

from typing import Callable, List, Optional, Union

from .models import Image, Task, DelayedTask, User, TaskResult, Role, Group


def _strip_group_domain(name):
    # Turns PPA's internal names like 'ad:your.domain.net:PPA Users' into 'PPA Users'
    try:
        name = re.search(r"^ad:[\w.]+:(.*)$", name).group(1)
    except AttributeError:
        # Regex didn't match, best not do anything to the name.
        pass
    return name


def _group_modifier(group):
    if all((group["name"].startswith("ad:"), group["source"] == "active-directory")):
        group["name"] = _strip_group_domain(group["name"])
    return group


def _user_role_modifier(item):
    new_groups = []
    for group in item.get("groups") or []:
        if group.startswith("ad:"):
            new_groups.append(_strip_group_domain(group))
            continue
        new_groups.append(group)
    item["groups"] = new_groups
    return item


def _creator(
    tuple_type: Union[Image, Task, User, TaskResult],
    results: Union[List[dict], dict],
    modifier: Optional[Callable] = None,
) -> Optional[List]:
    if results is None:
        return None

    def _create_named_tuple(item):
        if modifier is not None:
            item = modifier(item)
        return tuple_type(**{field: item.get(field) for field in list(tuple_type._fields)})

    if isinstance(results, list):
        return [_create_named_tuple(d) for d in results]
    elif isinstance(results, dict):
        return _create_named_tuple(results)
    else:
        raise TypeError(
            f"Can only create API records from a list or dictionary, received {type(results)}."
        )


def _sort(items, key, reverse: Optional[bool] = False):
    return (
        sorted(items, key=lambda x: getattr(x, key), reverse=reverse)
        if isinstance(items, list)
        else items
    )


def images(func: Callable) -> Callable:
    @functools.wraps(func)
    def _image_creator(*args, **kwargs) -> Optional[List[Image]]:
        return _sort(_creator(Image, func(*args, **kwargs)), "name")

    return _image_creator


def tasks(func: Callable) -> Callable:
    @functools.wraps(func)
    def _task_creator(*args, **kwargs) -> Optional[List[Task]]:
        return _sort(_creator(Task, func(*args, **kwargs)), "started_at", reverse=True)

    return _task_creator


def delayed_tasks(func: Callable) -> Callable:
    @functools.wraps(func)
    def _delayed_task_creator(*args, **kwargs) -> Optional[List[DelayedTask]]:
        return _sort(_creator(DelayedTask, func(*args, **kwargs)), "start_time", reverse=True)

    return _delayed_task_creator


def users(func: Callable) -> Callable:
    @functools.wraps(func)
    def _user_creator(*args, **kwargs) -> Optional[List[User]]:
        return _sort(_creator(User, func(*args, **kwargs), modifier=_user_role_modifier), "name")

    return _user_creator


def roles(func: Callable) -> Callable:
    @functools.wraps(func)
    def _role_creator(*args, **kwargs) -> Optional[List[Role]]:
        return _sort(_creator(Role, func(*args, **kwargs), modifier=_user_role_modifier), "name")

    return _role_creator


def groups(func: Callable) -> Callable:
    @functools.wraps(func)
    def _group_creator(*args, **kwargs) -> Optional[List[Group]]:
        return _sort(_creator(Group, func(*args, **kwargs), modifier=_group_modifier), "name")

    return _group_creator


def task_result(func: Callable) -> Callable:
    @functools.wraps(func)
    def _task_result_creator(*args, **kwargs) -> Optional[List[TaskResult]]:
        return _creator(TaskResult, func(*args, **kwargs))

    return _task_result_creator
