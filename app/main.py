from fastapi import FastAPI

from app.core.handlers import add_exception_handlers
from app.core.messages import AuthMessages
from app.crud import UserCRUD
from app.database import Base, engine
from app.dependencies import DbDep
from app.schemas import LoginSchema
from app.schemas import User as UserSchema, UserCreate
from app.core.security import create_access_token
from app.routers.router import api_router


app = FastAPI()

Base.metadata.create_all(bind=engine)


add_exception_handlers(app)

app.include_router(api_router)


@app.post("/register", response_model=UserSchema)
async def register(user: UserCreate, db: DbDep):
    return UserCRUD.create_user(
        db=db, email=user.email, password=user.password, full_name=user.full_name
    )


@app.post("/login")
async def login(data: LoginSchema, db: DbDep):
    user = UserCRUD.is_user_authenticated(db=db, data=data)

    access_token = create_access_token(user_id=user.id)

    return {
        "access_token": access_token,
        "type": "bearer",
        "message": AuthMessages.LOGIN_SUCCESS,
        "user": {"email": user.email, "full_name": user.full_name},
    }
