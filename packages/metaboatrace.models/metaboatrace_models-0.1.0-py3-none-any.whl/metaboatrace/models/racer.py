from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, StrictInt

from .region import Branch, Prefecture


class Gender(Enum):
    MALE = 1
    FEMALE = 2


class RacerRank(Enum):
    A1 = 1
    A2 = 2
    B1 = 3
    B2 = 4


class Racer(BaseModel):
    registration_number: StrictInt
    last_name: str
    first_name: str = ""
    gender: Optional[Gender]
    term: Optional[StrictInt]
    birth_date: Optional[date]
    height: Optional[StrictInt]
    born_prefecture: Optional[Prefecture]
    branch: Optional[Branch]


class RacerCondition(BaseModel):
    recorded_on: date
    racer_registration_number: StrictInt
    weight: StrictInt
    adjust: float
