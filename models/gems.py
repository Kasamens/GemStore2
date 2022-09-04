from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


class GemType(str, Enum):
    DIAMOND = 'DIAMOND'
    RUBY = 'RUBY'
    EMERALD = 'EMERALD'


class GemClarity(int, Enum):
    SI = 1
    VS = 2
    VVS = 3
    FL = 4


class GemColor(str, Enum):
    D = 'D'
    E = 'E'
    G = 'G'
    F = 'F'
    H = 'H'
    I = 'I'


class GemProperties(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    size: float
    clarity: Optional[GemClarity] = None
    color: Optional[GemColor] = None

    gem: Optional['Gem'] = Relationship(back_populates='gem_properties')


class BaseGem(SQLModel):
    price: float
    available: bool
    gem_type: GemType = GemType.DIAMOND


class GemCreate(BaseGem):
    pass


class GemOut(BaseGem):
    id: int


class GemUpdate(SQLModel):
    price: Optional[float] = None
    available: Optional[bool] = None
    gem_type: Optional[GemType] = None


class Gem(BaseGem, table=True):
    id: Optional[int] = Field(primary_key=True)

    gem_properties_id: Optional[int] = Field(
        default=None, foreign_key='gemproperties.id')
    gem_properties: Optional[GemProperties] = Relationship(
        back_populates='gem')
