import datetime
from pydantic import BaseModel


class SessionBase(BaseModel):
    user_id: int
    expires_at: datetime
    session_token: str


class Session(SessionBase):
    session_id: int

