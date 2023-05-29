from pydantic import BaseSettings


class Settings(BaseSettings):

    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'password'
    DB_HOST: str = 'localhost'
    DB_PORT: str = 5432
    DB_NAME: str = 'auth'

    @property
    def database_config(self) -> dict[str, str | int]:
        return {
            'database': self.DB_NAME,
            'user': self.DB_USER,
            'password': self.DB_PASSWORD,
            'host': self.DB_HOST,
            'port': self.DB_PORT,
        }

    @property
    def database_url(self):
        return 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(**self.database_config)

    SECRET_KEY: str = 'secret'
    ALGO: str = 'HS256'


settings = Settings()
