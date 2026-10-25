from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class TripCreate(BaseModel):

    destination: str

    start_date: date

    end_date: date

    travelers: int

    budget: Decimal

   


class TripUpdate(BaseModel):

    destination: str | None = None

    start_date: date | None = None

    end_date: date | None = None

    travelers: int | None = None

    budget: Decimal | None = None

   


class TripResponse(BaseModel):

    id: int

    user_id: int

    destination: str

    start_date: date

    end_date: date

    travelers: int

    budget: Decimal

 

    class Config:
        from_attributes = True