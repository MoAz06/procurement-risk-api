from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.database import SessionLocal
from app.models import User
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(user_data: RegisterRequest):
    db = SessionLocal()

    existing_user = db.query(User).filter(User.username == user_data.username).first()

    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        username=user_data.username,
        hashed_password=hash_password(user_data.password)
    )

    db.add(user)
    db.commit()
    db.close()

    return {"message": "User registered successfully"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()

    user = db.query(User).filter(User.username == form_data.username).first()
    db.close()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username
    }