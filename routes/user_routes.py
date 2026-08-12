from fastapi import APIRouter, Depends

from auth.dependencies import get_current_user

router = APIRouter()


@router.get("/me")
def get_me(
    current_user=Depends(get_current_user )
):

    return {

        "id": str(current_user["_id"]),

        "username": current_user["username"],

        "email": current_user["email"]

    }