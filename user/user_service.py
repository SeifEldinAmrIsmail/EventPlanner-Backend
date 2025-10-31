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
    # 1. check if this email already exists
    existing = repo.find_user_by_email(req.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 2. hash password
    pw_hash = hash_password(req.password)

    # 3. save to DB
    created = repo.create_user(req.email, pw_hash)
    if created is None:
        # safety if Mongo unique index blocks insert
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 4. return clean response
    return RegisterResponse(
        user_id=created["_id"],
        email=created["email"]
    )

def login_user(req: LoginRequest) -> LoginResponse:
    # 1. find user in DB
    user = repo.find_user_by_email(req.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 2. check password
    if not verify_password(req.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 3. create JWT access token
    token = create_access_token(
        user_id=user["_id"],
        email=user["email"]
    )

    # 4. return login response
    return LoginResponse(
        access_token=token,
        user_id=user["_id"],
        email=user["email"]
    )
