from http import HTTPStatus

from django.shortcuts import get_object_or_404
from ninja import Router

from core.models import Project
from core.models import Tag
from core.models import State
from core.schemas import UseProject
from core.schemas import NewProject
from core.schemas import PushProject
from core.schemas import SetProject
from core.schemas import DropProject

# TODO - logs, permissions


router = Router()


@router.post("/use/", response={HTTPStatus.ACCEPTED: dict})
def use(request, payload: UseProject):
    user = request.auth
    name = Project.normalize_str(payload.name)
    instance = get_object_or_404(Project, organization=user.organization, name=name)
    user.project = instance
    user.save()
    return HTTPStatus.ACCEPTED, {"detail": f"Project [{instance.name}] selected."}


@router.post("/new/", response={HTTPStatus.CREATED: dict, HTTPStatus.CONFLICT: dict})
def new(request, payload: NewProject):
    user = request.auth
    if Project.objects.filter(organization=user.organization, name=Project.normalize_str(payload.name)).exists():
        return HTTPStatus.CONFLICT, {"detail": f"Project [{payload.name}] already exists."}
    instance = Project(organization=user.organization)
    for field, value in payload.dict().items():
        if value:
            if field != "tags" and value is not None:
                setattr(instance, field, value)
    instance.save()
    normalized_tags = list(map(Tag.normalize_str, payload.tags))
    tags_queryset = Tag.objects.filter(organization=user.organization, name__in=normalized_tags)
    new_tags = []
    for tag_name in filter(lambda tag_name: not tags_queryset.filter(name=tag_name).exists(), normalized_tags):
        new_tags.append(Tag(organization=user.organization, name=tag_name))

    Tag.objects.bulk_create(new_tags)
    instance.tags.add(*tags_queryset, *new_tags)

    return HTTPStatus.CREATED, {"detail": "Project created."}


@router.post("/set/", response={HTTPStatus.ACCEPTED: dict, HTTPStatus.BAD_REQUEST: dict})
def set(request, payload: SetProject):
    user = request.auth
    if not user.project:
        return HTTPStatus.BAD_REQUEST, {"detail": "No project in use."}
    name = State.normalize_str(payload.state)
    state = get_object_or_404(State, organization=user.organization, name=name)
    user.project.state = state
    user.project.save()
    return HTTPStatus.ACCEPTED, {"detail": f"[{user.project.name}] set [{payload.state}]."}


@router.delete("/drop/", response={HTTPStatus.OK: dict})
def drop(request, payload: DropProject):
    user = request.auth
    name = State.normalize_str(payload.name)
    instance = get_object_or_404(Project, organization=user.organization, name=name)
    instance.delete()
    return HTTPStatus.OK, {"detail": "Project deleted."}


@router.put("/push/", response={HTTPStatus.ACCEPTED: dict, HTTPStatus.BAD_REQUEST: dict})
def push(request, payload: PushProject):
    user = request.auth
    if not user.project:
        return HTTPStatus.BAD_REQUEST, {"detail": "No project in use."}

    instance = get_object_or_404(Project, organization=user.organization, id=user.project.id)
    instance.tags.clear()

    for field, value in payload.dict().items():
        if value:
            if field != "tags" or value is not None:
                setattr(instance, field, value)
    instance.save()

    normalized_tags = list(map(Tag.normalize_str, payload.tags))
    tags_queryset = Tag.objects.filter(organization=user.organization, name__in=normalized_tags)
    new_tags = []
    for tag_name in filter(lambda tag_name: not tags_queryset.filter(name=tag_name).exists(), normalized_tags):
        new_tags.append(Tag(organization=user.organization, name=tag_name))

    Tag.objects.bulk_create(new_tags)
    instance.tags.add(*tags_queryset, *new_tags)

    return HTTPStatus.ACCEPTED, {"detail": "Project changes accepted."}


@router.get("/pull/", response={HTTPStatus.OK: dict, HTTPStatus.BAD_REQUEST: dict})
def pull(request):
    user = request.auth
    if not user.project:
        return HTTPStatus.BAD_REQUEST, {"detail": "No project in use."}
    return HTTPStatus.OK, next(iter(Project.objects.hydrate(id=user.project.id)), {})
