from pydantic import BaseModel, PositiveInt, constr, NonNegativeInt


class OrmModel(BaseModel):
    class Config:
        orm_mode = True


class MessageOnlyContent(OrmModel):
    Content: constr(max_length=160)


class MessageNoCounter(OrmModel):
    MessageID: PositiveInt
    Content: constr(max_length=160)


class MessageNoID(OrmModel):
    Content: constr(max_length=160)
    Counter: NonNegativeInt


class Message(OrmModel):
    MessageID: PositiveInt
    Content: constr(max_length=160)
    Counter: NonNegativeInt


class Account(OrmModel):
    AccountID: PositiveInt
    Login: constr(max_length=30)
    PasswordHash: constr(max_length=128)
