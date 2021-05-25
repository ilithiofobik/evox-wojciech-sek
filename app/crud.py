from sqlalchemy import update, func, insert, delete
from sqlalchemy.orm import Session

from .models import Message
from . import models, schemas


def check_account(db: Session, login: str, password_hash: str):
    return db.query(models.Account).filter(models.Account.PasswordHash == password_hash) \
        .filter(models.Account.Login == login).first()


def create_message(db: Session, new_message: schemas.MessageOnlyContent):
    db.execute(insert(models.Message).values({Message.Content: new_message.Content}))
    db.commit()
    return {"id": db.query(func.max(models.Message.MessageID)).scalar()}


def update_message(db: Session, new_message: schemas.MessageNoCounter):
    db.execute(update(models.Message).where(models.Message.MessageID == new_message.MessageID)
               .values({Message.Content: new_message.Content, Message.Counter: 0}))
    db.commit()
    return {"Result": "Updated successfully"}


def delete_message(db: Session, message_id: int):
    db.execute(delete(models.Message).where(models.Message.MessageID == message_id))
    db.commit()
    return {"Result": "Deleted successfully"}


def counter_inc(db: Session, message_id: int):
    db.execute(update(models.Message).where(models.Message.MessageID == message_id)
               .values({Message.Counter: Message.Counter + 1}))
    db.commit()


def get_messages_id(db: Session, message_id: int):
    counter_inc(db, message_id)
    return db.query(models.Message).filter(models.Message.MessageID == message_id).first()
