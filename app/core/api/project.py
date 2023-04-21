from ninja import Router


router = Router()


@router.get("/")
def project_sync(request):

    return {
        "status_code": 200,
        "message": "Under Construction!"
    }

