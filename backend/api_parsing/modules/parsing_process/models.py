import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime

from core.database.database import Base


class Proces(Base):
    """Описание таблицы базы данных процесса парсинга"""

    id = Column(Integer, primary_key=True)
    iterate = Column(Integer, default=0)
    page = Column(Integer, default=1)
    error = Column(Boolean, default=False)
    created_ad = Column(DateTime, default=datetime.datetime.now())
