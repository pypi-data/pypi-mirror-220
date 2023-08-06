from collections import namedtuple

Image = namedtuple(
    "Image",
    [
        "author",
        "description",
        "deployed",
        "groups",
        "id",
        "name",
        "owner",
        "tags",
        "updated_at",
        "uuid",
    ],
)

Task = namedtuple(
    "Task",
    [
        "author",
        "cancelled_at",
        "cancelled_by",
        "deployed",
        "duration",
        "exit_code",
        "exit_message",
        "id",
        "image",
        "image_id",
        "image_uuid",
        "is_owner",
        "is_running",
        "started_at",
        "state",
        "stopped_at",
        "timed_out",
        "timeout",
        "trigger",
        "username",
        "uuid",
    ],
)


DelayedTask = namedtuple(
    "DelayedTask",
    [
        "description",
        "id",
        "image",
        "image_id",
        "is_owner",
        "is_pending",
        "payload",
        "start_time",
        "task_uuid",
        "timezone",
        "trigger",
        "username",
    ],
)

User = namedtuple(
    "User",
    [
        "active",
        "authenticated_at",
        "deleted_at",
        "email",
        "id",
        "name",
        "username",
        "groups",
        "permissions",
        "roles_count",
    ],
)

Role = namedtuple("Role", ["id", "name", "groups", "groups_count", "users_count", "permissions"])

Group = namedtuple(
    "Group",
    [
        "id",
        "name",
        "source",
        "user_sync",
        "start_tasks",
        "roles_count",
        "images_count",
        "members_count",
    ],
)

TaskResult = namedtuple("TaskResult", ["exit_code", "exit_message", "result_json", "state"])
