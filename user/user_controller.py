from fastapi import APIRouter
from user.user_models import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse
)
from user.user_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=RegisterResponse)
def register_endpoint(req: RegisterRequest):
    return register_user(req)

@router.post("/login", response_model=LoginResponse)
def login_endpoint(req: LoginRequest):
    return login_user(req)
