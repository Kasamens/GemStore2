import email
from fastapi import APIRouter, HTTPException, Depends, status
from auth.auth import AuthHandler
from models.user import UserInput, User
from database import get_session
from sqlmodel import Session, select
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

router = APIRouter()
auth_handler = AuthHandler()


@router.post('/registration', status_code=201, tags=['users'],
             description='Register new user')
async def register(user: UserInput, session: Session = Depends(get_session)):
    query = select(User)
    users = session.exec(query).all()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = auth_handler.get_password_hash(user.password)
    u = User()
    u.username = user.username
    u.password = hashed_pwd
    u.email = user.email
    u.is_seller = user.is_seller

    session.add(u)
    session.commit()
    return JSONResponse(status_code=HTTP_201_CREATED)
