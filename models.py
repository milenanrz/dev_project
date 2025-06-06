from typing import Optional
from datetime import datetime, date
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel
from terms import *

class PhotographerBase(SQLModel):
    name: Optional[str] = Field(min_length=3, max_length=20)
    genre: Optional[Genre] = Field(default=None)
    nationality: Optional[Nationality] = Field(default=None)
    photographic_style_name: Optional[PhotographicStyle]= Field(default=None)
    is_alive: Optional[bool] = Field(default=True)

    #new
    photographer_image_path: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=None)

class PhotographerSQL(PhotographerBase, table=True):
    __tablename__ = "photographers"
    id: Optional[int] = Field(default=None, primary_key=True)
    model_config = ConfigDict(from_attributes=True)

class PortfolioBase(SQLModel):
    photographer_id: Optional[int] = Field(foreign_key="photographers.id")
    title: Optional[str] = Field(min_length=1, max_length=50)
    category: Optional[PhotographicStyle] = Field(default=None)
    photo_created_at: Optional[date] = Field(default=None)

    #new
    portfolio_image_path: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=None)


class PortfolioSQL(PortfolioBase, table=True):
    __tablename__ = "portfolios"
    id: Optional[int] = Field(default=None, primary_key=True)
    model_config = ConfigDict(from_attributes=True)
