from fastapi import HTTPException, status
from core.security import hash_password, verify_password, create_access_token
from user.user_models import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse
)
from user import user_repository as repo

def register_user(req: RegisterRequest) -> RegisterResponse:
    existing = repo.find_user_by_email(req.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )


    pw_hash = hash_password(req.password)

    created = repo.create_user(req.email, pw_hash)
    if created is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    return RegisterResponse(
        user_id=created["_id"],
        email=created["email"]
    )

def login_user(req: LoginRequest) -> LoginResponse:
    user = repo.find_user_by_email(req.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(req.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(
        user_id=user["_id"],
        email=user["email"]
    )

    return LoginResponse(
        access_token=token,
        user_id=user["_id"],
        email=user["email"]
    )
