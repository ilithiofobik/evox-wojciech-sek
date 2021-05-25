from sqlalchemy import (
    Column,
    Date,
    Float,
    Integer,
    LargeBinary,
    SmallInteger,
    String,
    Table,
    Text,
    text,
    Sequence,
    CheckConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import NullType

Base = declarative_base()
metadata = Base.metadata


MESSAGE_ID_SEQ = Sequence('message_id_seq')  # define sequence explicitly
ACCOUNT_ID_SEQ = Sequence('account_id_seq')  # define sequence explicitly



class Message(Base):
    __tablename__ = "messages"

    MessageID = Column(Integer, primary_key=True, nullable=False, server_default=MESSAGE_ID_SEQ.next_value())
    Content = Column(String(160), nullable=False)
    Counter = Column(Integer, nullable=False, server_default='0')
    CheckConstraint('length(Content) > 0')


class Account(Base):
    __tablename__ = "accounts"

    AccountID = Column(Integer, primary_key=True, server_default=ACCOUNT_ID_SEQ.next_value())
    Login = Column(String(30), nullable=False)
    PasswordHash = Column(String(128), nullable=False)