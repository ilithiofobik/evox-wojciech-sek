from hashlib import sha512
import string
import random
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import HTTPBasic
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db

router = APIRouter()
router.session_tokens = []
security = HTTPBasic()


def random_token():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(32))


@router.get("/login", status_code=status.HTTP_202_ACCEPTED)
def get_auth(response: Response, login: str, password: str, db: Session = Depends(get_db)):
    password_hash = str(sha512(password.encode("utf-8")).hexdigest())
    check = crud.check_account(db, login, password_hash)

    if not check:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    session_token = random_token()
    response.set_cookie(key="session_token", value=session_token)
    router.session_tokens.append(session_token)
    return {"message": "welcome"}


@router.delete("/logout", status_code=status.HTTP_202_ACCEPTED)
def logout(session_token: str = Cookie(None)):
    if session_token not in router.session_tokens:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    router.session_tokens.remove(session_token)
    return {"message": "goodbye"}


@router.post("/messages", status_code=status.HTTP_201_CREATED)
async def create_message(new_message: schemas.MessageOnlyContent, session_token: str = Cookie(None),
                         db: Session = Depends(get_db)):
    if session_token not in router.session_tokens:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised")
    return crud.create_message(db, new_message)


@router.put("/messages", status_code=status.HTTP_202_ACCEPTED)
async def update_message(new_message: schemas.MessageNoCounter, session_token: str = Cookie(None),
                         db: Session = Depends(get_db)):
    if session_token not in router.session_tokens:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised")
    if not crud.get_messages_id(db, new_message.MessageID):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return crud.update_message(db, new_message)


@router.delete("/messages/{message_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_message(message_id: PositiveInt, session_token: str = Cookie(None), db: Session = Depends(get_db)):
    if session_token not in router.session_tokens:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised")
    if not crud.get_messages_id(db, message_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return crud.delete_message(db, message_id)


@router.get("/messages/{message_id}", response_model=schemas.MessageNoID)
async def get_messages_id(message_id: PositiveInt, db: Session = Depends(get_db)):
    message = crud.get_messages_id(db, message_id)
    if message:
        return message
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
