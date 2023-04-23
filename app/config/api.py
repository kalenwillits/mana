from ninja import NinjaAPI
from django.contrib import auth


from core.api.client import router as project_router


def authenticate(request):
    user = auth.authenticate(
        username=request.headers.get("username"),
        password=request.headers.get("password")
    )
    if not user.organization:
        return
    return user


api = NinjaAPI(auth=authenticate)

api.add_router("/project/", project_router)
