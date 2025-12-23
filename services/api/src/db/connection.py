from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

from settings import settings


@contextmanager
def get_conn():
    if not settings.database_url:
        raise RuntimeError("DATABASE_URL is required to use the database")
    with psycopg.connect(settings.database_url, row_factory=dict_row) as conn:
        yield conn
