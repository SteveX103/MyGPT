from fastapi import APIRouter, HTTPException

from database.mongodb import users_collection

from models.user_model import RegisterUser, LoginUser

from auth.password_handler import (
    hash_password,
    verify_password
)

from auth.jwt_handler import create_access_token

router = APIRouter()


@router.post("/register")
def register(user: RegisterUser):

    existing = users_collection.find_one(
        {
            "email": user.email
        }
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    users_collection.insert_one({

        "username": user.username,

        "email": user.email,

        "password": hash_password(
            user.password
        )

    })

    return {
        "message": "Registration successful"
    }


@router.post("/login")
def login(user: LoginUser):

    db_user = users_collection.find_one(
        {
            "email": user.email
        }
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        user.password,
        db_user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token({

        "user_id": str(
            db_user["_id"]
        ),

        "email": db_user["email"]

    })

    return {

        "access_token": token,

        "token_type": "bearer"

    }