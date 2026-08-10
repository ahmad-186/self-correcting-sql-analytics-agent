from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.config.settings import settings

engine : Engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    echo=False
)