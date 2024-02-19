import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LinkBaseSchema(BaseModel):
    id: int
    link: str = Field(..., title="Ссылка")
    price: int
    title: str
    status_id: int
    is_video: bool
    comment: Optional[str] = None
    link_img: Optional[str] = None
    created_ad: datetime.datetime

    class Config:
        from_attributes = True


class NewLinkSchema(BaseModel):
    link: str = Field(..., title="Ссылка")
    price: int
    title: str
    status_id: int = 0
    is_video: bool
    comment: Optional[str] = None
    link_img: Optional[str] = None

    class Config:
        from_attributes = True


class ReadLinkSchema(LinkBaseSchema):
    pass


class UpdateLinkSchema(LinkBaseSchema):
    pass
