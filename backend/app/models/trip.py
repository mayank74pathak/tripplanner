from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Numeric,
    ForeignKey,
    DateTime
)
from sqlalchemy.sql import func

from app.database import Base


class Trip(Base):

    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    destination = Column(
        String(100),
        nullable=False
    )

    start_date = Column(
        Date,
        nullable=False
    )

    end_date = Column(
        Date,
        nullable=False
    )

    travelers = Column(
        Integer,
        nullable=False
    )

    budget = Column(
        Numeric(12, 2),
        nullable=False
    )

     

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )