from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from backend.auth import hash_password, verify_password
from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models import User
from backend.schemas import UserCreate, UserLogin, UserOut

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email.lower()).first()
    if existing_user:
        raise ValueError("Email is already registered")

    user = User(
        full_name=user_data.full_name.strip(),
        email=user_data.email.lower(),
        password_hash=hash_password(user_data.password),
        role="regular",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=UserOut)
def login_user(
    login_data: UserLogin,
    response: Response,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == login_data.email.lower()).first()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise ValueError("Invalid email or password")

    response.set_cookie(
        key="user_id",
        value=str(user.id),
        httponly=True,
        secure=True,
        samesite="none",
    )
    return user


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="user_id",
        secure=True,
        samesite="none",
    )
    return {"message": "Logged out successfully"}