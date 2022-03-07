import os


class Config:
    OMDBAPI_KEY: str
    DB_SQLITE_DIR: str
    API_PORT: int

    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFUALT_TIMEOUT = 5*60

    def __init__(self):
        self.DB_SQLITE_DIR = self._get_environ("DB_SQLITE_DIR")
        self.OMDBAPI_KEY = self._get_environ("OMDBAPI_KEY")
        self.API_PORT = self._get_environ("API_PORT")

    @staticmethod
    def _get_environ(keyword: str):
        var = os.environ.get(keyword)
        if not var:
            raise RuntimeError(f'{keyword} environment variable not setup.')
        else:
            return var

