import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime

from core.database.database import Base


class Link(Base):
    """Описание таблицы базы данных объявлений недвижимости при парсинге"""

    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True, nullable=False)
    price = Column(Integer, nullable=True)
    title = Column(String, nullable=False)
    status_id = Column(Integer, default=0)
    is_video = Column(Boolean, default=False)
    comment = Column(String, nullable=True, default=None)
    link_img = Column(String, nullable=True, default=None)
    created_ad = Column(DateTime, default=datetime.datetime.now())
