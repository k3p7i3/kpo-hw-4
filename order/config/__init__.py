from pydantic import BaseSettings


class Settings(BaseSettings):

    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 2567 #'password'
    DB_HOST: str = 'localhost'
    DB_PORT: str = 5432
    DB_NAME: str = 'order'

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

    AUTH_DOMAIN = 'auth'
    AUTH_PORT = 8000

    @property
    def auth_url(self):
        return f'http://{self.AUTH_DOMAIN}:{self.AUTH_PORT}'


settings = Settings()
