from http import HTTPStatus

from django.shortcuts import get_object_or_404
from ninja import Router

from core.models import Project
from core.models import Tag
from core.state import State
from core.schemas import NewProject
from core.schemas import PushProject


router = Router()


@router.post("/use/")
def use(request, name: str):
    user = request.auth
    instance = get_object_or_404.NOT_FOUND(Project, organization=user.organization, name=name)
    user.project = instance
    user.save()
    return HTTPStatus.ACCEPTED


@router.post("/new/")
def new(request, payload: NewProject):
    user = request.auth
    instance = Project(organization=user.organization)
    for field, value in payload.dict().items():
        if value:
            if field != "tags" or value is not None:
                setattr(instance, field, value)
    instance.save()

    tags_queryset = Tag.objects.filter(organization=user.organization, name__in=payload["tags"])
    new_tags = []
    for tag_name in filter(lambda tag_name: not tags_queryset.filter(name=tag_name).exists(), payload["tags"]):
        new_tags.append(Tag(organization=user.organization, name=tag_name))

    Tag.objects.bulk_create(new_tags)
    instance.tags.add(*tags_queryset, *new_tags)

    return HTTPStatus.CREATED


@router.post("/set/")
def set(request, state_name: str):
    user = request.auth
    if not user.project:
        return 400
    state = get_object_or_404.NOT_FOUND(State, organization=user.organization, name=state_name)
    user.project.state = state
    user.project.save()
    return HTTPStatus.CREATED


@router.delete("/drop/")
def drop(request, name: str):
    user = request.auth
    instance = get_object_or_404(Project, organization=user.organization, name=name)
    instance.delete()
    return HTTPStatus.OK


@router.put("/push/")
def push(request, payload: PushProject):
    user = request.auth
    if not user.project:
        return 400

    instance = get_object_or_404(Project, organization=user.organization, id=user.project.id)
    instance.tags.clear()

    for field, value in payload.dict().items():
        if value:
            if field != "tags" or value is not None:
                setattr(instance, field, value)
    instance.save()

    tags_queryset = Tag.objects.filter(organization=user.organization, name__in=payload["tags"])
    new_tags = []
    for tag_name in filter(lambda tag_name: not tags_queryset.filter(name=tag_name).exists(), payload["tags"]):
        new_tags.append(Tag(organization=user.organization, name=tag_name))

    Tag.objects.bulk_create(new_tags)
    instance.tags.add(*tags_queryset, *new_tags)

    return HTTPStatus.ACCEPTED


@router.get("/pull/")
def pull(request):
    user = request.auth
    if not user.project:
        return 400
    return HTTPStatus.OK, Project.objects.hydrate(id=user.project.id)
