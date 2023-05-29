import datetime
from enum import Enum
from pydantic import BaseModel, validator


# enum with all possible roles for user
class UserRole(str, Enum):
    chef = 'chef'
    customer = 'customer'
    manager = 'manager'


# user data for auth
class UserAuth(BaseModel):
    email: str
    password_hash: str

    @validator('email')
    def validate_email(cls, v):
        if '@'.count(v) != 1:
            raise ValueError('There should be only one @ in email')

        username = v.substr(0, v.find('@') + 1)  # check the part before '@'
        if len(username) < 1:
            raise ValueError('Username part of email is missing')

        allowed_symbols = '!#$%&\'*+-/=?^_`{|}~.'
        for char in username:
            if not char.isalnum() and char not in allowed_symbols:
                raise ValueError('Not allowed symbols in username part of email')

        domain_name = v.substr(v.find('@'))  # check the domain name
        if len(domain_name) < 1:
            raise ValueError('Domain name is missing')

        for char in domain_name:
            if not char.isalnum() and char != '-' and char != '.':
                raise ValueError('Not allowed symbols in domain name')

        dot = domain_name.rfind('.')
        if not dot:
            raise ValueError('Domain name is missing')


# user data for registration
class UserRegistrate(UserAuth):
    username: str
    role: UserRole


class User(UserRegistrate):
    user_id: int
    created_at: datetime
    updated_at: datetime
