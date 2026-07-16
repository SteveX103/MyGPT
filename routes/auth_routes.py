from fastapi import APIRouter
from database.mongodb import users_collection
from models.user_model import RegisterUser
from auth.password_handler import hash_password
from models.user_model import LoginUser
from auth.password_handler import verify_password
from auth.jwt_handler import create_access_token


router = APIRouter()


@router.post("/register")
def register(user: RegisterUser):

    existing = users_collection.find_one(
        {"email": user.email}
    )

    if existing:
        return {
            "message": "User already exists"
        }

    users_collection.insert_one({

        "username": user.username,

        "email": user.email,

        "password":
            hash_password(
                user.password
            )
    })

    return {
        "message":
            "User created"
    }


@router.post("/login")
def login(user: LoginUser):

    db_user = users_collection.find_one(
        {"email": user.email}
    )

    if not db_user:
        return {
            "message": "Invalid credentials"
        }

    if not verify_password(
        user.password,
        db_user["password"]
    ):
        return {
            "message": "Invalid credentials"
        }

    token = create_access_token({

        "id": str(db_user["_id"]),

        "email":
            db_user["email"]
    })

    return {
        "access_token": token
    }