import datetime
import hashlib
from fastapi import HTTPException
from jose import jwt, JWTError
from asyncpg.exceptions import UniqueViolationError

from auth.config import settings
from auth.db.gateway import UserGateway, SessionGateway
from auth.models import (
    Session,
    SessionBase,
    User,
    UserAuth,
    UserInfo,
    UserRegistrate,
)


class UserLogic:
    def __init__(self):
        self.db_users = UserGateway()
        self.db_sessions = SessionGateway()

    async def _does_username_exist(self, username: str) -> bool:
        user: User = await self.db_users.get_user_by_username(username)
        return user is not None

    async def _does_email_exist(self, email: str) -> bool:
        user: User = await self.db_users.get_user_by_email(email)
        return user is not None

    def _hash_password(self, password: str) -> str:
        hash_password: str = hashlib.sha512(password.encode()).hexdigest()
        return hash_password

    async def _generate_token(self, user_id: int) -> str:
        payload = {'iat': datetime.datetime.utcnow()}
        encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGO)

        expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        session: SessionBase = SessionBase(
            user_id=user_id,
            expires_at=expires_at,
            session_token=encoded_jwt,
        )
        session_id: int = await self.db_sessions.create_session(session)
        if not session_id:
            raise HTTPException(status_code=500, detail='Can\'t create access token')

        return encoded_jwt

    async def _create_user(self, user: UserRegistrate) -> int:
        try:
            user_id: int = await self.db_users.create_user(user)
        except UniqueViolationError:
            if await self._does_username_exist(user.username):
                raise HTTPException(status_code=400, detail='User with this username already exist')
            if await self._does_email_exist(user.email):
                raise HTTPException(status_code=400, detail='User with this email already exist')
            raise HTTPException(status_code=500, detail='Registration failed')

        return user_id

    async def _identify_user_by_login(self, user: UserAuth) -> int:
        user: User = await self.db_users.get_user_by_auth(auth_user=user)
        if not user:
            raise HTTPException(status_code=400, detail='Wrong email or password')
        return user.user_id

    async def _auth_by_jwt_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGO)
        except JWTError:
            raise HTTPException(status_code=401, detail='Invalid access token')

        session: Session = await self.db_sessions.get_session_by_token(token)
        if not session:
            raise HTTPException(status_code=401, detail='Token does not exist')

        if session.expires_at < datetime.datetime.utcnow():
            raise HTTPException(status_code=401, detail='Token expired')

        return session.user_id

    async def _get_user_info(self, user_id: int) -> UserInfo:
        user: User = await self.db_users.get_user(user_id)
        if not user:
            raise HTTPException(status_code=500, detail='User does not exist')

        return UserInfo(
            user_id=user_id,
            username=user.username,
            email=user.email,
            role=user.role,
        )

    async def get_user_info_by_token(self, token: str) -> UserInfo:
        user_id: int = await self._auth_by_jwt_token(token)
        return await self._get_user_info(user_id)

    async def registrate_user(self, user: UserRegistrate) -> str:
        user.password_hash = self._hash_password(user.password_hash)
        user_id = await self._create_user(user)
        token = await self._generate_token(user_id)
        return token

    async def login_user(self, user: UserAuth) -> str:
        user.password_hash = self._hash_password(user.password_hash)
        user_id = await self._identify_user_by_login(user)
        token = await self._generate_token(user_id)
        return token
