from pydantic import BaseModel, PositiveInt, constr, NonNegativeInt


class MessageOnlyContent(BaseModel):
    Content: str


class MessageNoCounter(BaseModel):
    MessageID: PositiveInt
    Content: constr(max_length=160)

    class Config:
        orm_mode = True



class MessageNoID(BaseModel):
    Content: constr(max_length=160)
    Counter: NonNegativeInt

    class Config:
        orm_mode = True


class Message(BaseModel):
    MessageID: PositiveInt
    Content: constr(max_length=160)
    Counter: NonNegativeInt

    class Config:
        orm_mode = True


class Account(BaseModel):
    AccountID: PositiveInt
    Login: constr(max_length=30)
    PasswordHash: constr(max_length=128)

    class Config:
        orm_mode = True
