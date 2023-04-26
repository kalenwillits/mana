from http import HTTPStatus
from datetime import datetime

from django.shortcuts import get_object_or_404
from ninja import Router

from core.models import Task
from core.models import State
from core.models import Log
from core.models import Comment
from core.schemas import UseTaskIn
from core.schemas import NewTaskIn
from core.schemas import PushTaskIn
from core.schemas import SetTaskIn
from core.schemas import DropTaskIn
from core.schemas import PullTaskOut
from core.schemas import PullCommentOut


router = Router()


@router.put("/use/", response={
        HTTPStatus.ACCEPTED: dict
    }
)
def use(request, payload: UseTaskIn):
    timestamp = datetime.utcnow()
    user = request.auth
    user.read_at = timestamp
    old_task = user.task
    name = Task.normalize_str(payload.name)
    instance = get_object_or_404(
        Task,
        organization=user.organization,
        name=name
    )
    instance.read_at = timestamp
    user.task = instance
    user.save()
    Log(
        organization=user.organization,
        info=f"use [{old_task}] -> [{user.task}]",
        user=user,
        link=instance,
    ).save()
    return HTTPStatus.ACCEPTED, {"detail": "Task selected."}


@router.post("/new/", response={
        HTTPStatus.CREATED: dict,
        HTTPStatus.CONFLICT: dict
    }
)
def new(request, payload: NewTaskIn):
    timestamp = datetime.utcnow()
    user = request.auth
    user.read_at = timestamp
    user.save()
    if Task.objects.filter(organization=user.organization, name=Task.normalize_str(payload.name)).exists():
        return HTTPStatus.CONFLICT, {"detail": f"Task [{payload.name}] already exists."}
    instance = Task(
        organization=user.organization,
        owner=user.role,
        sprint=user.sprint,
    ).update(**payload.dict()).save()
    Log(
        organization=user.organization,
        info=f"new [{instance}]",
        user=user,
        link=instance,
    ).save()

    return HTTPStatus.CREATED, {"detail": "Task created."}


@router.put("/set/", response={
        HTTPStatus.ACCEPTED: dict,
        HTTPStatus.BAD_REQUEST: dict,
        HTTPStatus.UNAUTHORIZED: dict
    }
)
def set(request, payload: SetTaskIn):
    timestamp = datetime.utcnow()
    user = request.auth
    user.read_at = timestamp
    user.save()
    if not user.task:
        return HTTPStatus.BAD_REQUEST, {"detail": "No task in use."}
    old_state = user.task.state
    name = State.normalize_str(payload.state)
    state = get_object_or_404(
        State,
        organization=user.organization,
        name=name,
    )
    state.read_at = timestamp
    if state.role != user.role:
        return HTTPStatus.UNAUTHORIZED, {"detail": "Unauthorized action."}
    user.task.state = state
    user.task.updated_at = timestamp
    user.task.save()
    Log(
        organization=user.organization,
        info=f"set [{old_state}] -> [{state}]",
        user=user,
        link=user.task,
    ).save()
    return HTTPStatus.ACCEPTED, {"detail": f"[{user.project}] set [{payload.state}]."}


@router.delete("/drop/", response={
        HTTPStatus.OK: dict,
        HTTPStatus.UNAUTHORIZED: dict
    }
)
def drop(request, payload: DropTaskIn):
    timestamp = datetime.utcnow()
    user = request.auth
    user.updated_at = timestamp
    user.save()
    name = State.normalize_str(payload.name)
    instance = get_object_or_404(Task, organization=user.organization, name=name)
    if instance.owner != user.role:
        return HTTPStatus.UNAUTHORIZED, {"detail": "Unauthorized action."}
    instance.delete()
    Log(
        organization=user.organization,
        info=f"drop [{instance}]",
        user=user,
        link=None,
    ).save()
    return HTTPStatus.OK, {"detail": "Task deleted."}


@router.put("/push/", response={
        HTTPStatus.ACCEPTED: dict,
        HTTPStatus.BAD_REQUEST: dict,
        HTTPStatus.UNAUTHORIZED: dict
    }
)
def push(request, payload: PushTaskIn):
    timestamp = datetime.utcnow()
    user = request.auth
    user.read_at = timestamp
    user.save()
    if not user.task:
        return HTTPStatus.BAD_REQUEST, {"detail": "No task in use."}
    instance = get_object_or_404(
        Task,
        organization=user.organization,
        id=user.task.id
    )
    if instance.owner != user.role:
        return HTTPStatus.UNAUTHORIZED, {"detail": "Unauthorized action."}
    instance.updated_at = timestamp
    instance.update(**payload.dict()).save()
    Log(
        organization=user.organization,
        info=f"push [{instance}]",
        user=user,
        link=instance,
    ).save()
    return HTTPStatus.ACCEPTED, {"detail": "Task changes accepted."}


@router.get("/pull/", response={
        HTTPStatus.OK: PullTaskOut,
        HTTPStatus.BAD_REQUEST: dict
    }
)
def pull(request):
    timestamp = datetime.utcnow()
    user = request.auth
    user.read_at = timestamp
    user.save()
    if not user.task:
        return HTTPStatus.BAD_REQUEST, {"detail": "No task in use."}
    task_queryset = Task.objects.filter(
        organization=user.organization, id=user.task.id
    )
    task_comment_queryset = Comment.objects.filter(
        organization=user.organization,
        task=user.task
    ).order_by("created_at")
    task_queryset.update(read_at=timestamp).save()
    task_comment_queryset.update(read_at=timestamp).save()
    Log(
        organization=user.organization,
        info=f"pull task [{user.task}]",
        user=user,
        link=task_queryset.first(),
    ).save()
    response = task_queryset.values(*PullTaskOut.fields()).first()
    response["comments"] = list(task_comment_queryset.values(*PullCommentOut.fields()))
    return HTTPStatus.OK, response
