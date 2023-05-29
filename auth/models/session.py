import datetime
from pydantic import BaseModel


class Token(BaseModel):
    session_token: str


class SessionBase(Token):
    user_id: int
    expires_at: datetime


class Session(SessionBase):
    session_id: int

