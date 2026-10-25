
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from openai import OpenAIError

from app.database import get_db
from app.models.trip import Trip
from app.models.user import User
from app.models.itinerary import Itinerary
from app.schemas.trip import TripCreate, TripUpdate
from app.services.auth_service import get_current_user
from app.services.itinerary_service import generate_itinerary


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/trips",
    tags=["Trips"]
)


# ============================================================
# CREATE TRIP
# ============================================================

@router.post("/")
def create_trip(
    trip_data: TripCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trip = Trip(
        user_id=current_user.id,
        destination=trip_data.destination,
        start_date=trip_data.start_date,
        end_date=trip_data.end_date,
        travelers=trip_data.travelers,
        budget=trip_data.budget,
    )

    db.add(trip)
    db.commit()
    db.refresh(trip)

    return trip


# ============================================================
# GET ALL TRIPS OF CURRENT USER
# ============================================================

@router.get("/")
def get_trips(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Trip).filter(
        Trip.user_id == current_user.id
    ).all()


# ============================================================
# GET ONE TRIP
# ============================================================

@router.get("/{trip_id}")
def get_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.user_id == current_user.id
    ).first()

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )

    return trip


# ============================================================
# UPDATE TRIP
# ============================================================

@router.put("/{trip_id}")
def update_trip(
    trip_id: int,
    trip_data: TripUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.user_id == current_user.id
    ).first()

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )

    update_data = trip_data.model_dump(exclude_unset=True)

    if "interests" in update_data:
        interests = update_data["interests"]
        update_data["interests"] = (
            ",".join(interests)
            if interests is not None
            else None
        )

    for key, value in update_data.items():
        setattr(trip, key, value)

    db.commit()
    db.refresh(trip)

    return trip


# ============================================================
# DELETE TRIP
# ============================================================

@router.delete("/{trip_id}")
def delete_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.user_id == current_user.id
    ).first()

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )

    # Delete the associated itinerary first.
    db.query(Itinerary).filter(
        Itinerary.trip_id == trip.id
    ).delete(synchronize_session=False)

    db.delete(trip)
    db.commit()

    return {"message": "Trip deleted successfully"}


# ============================================================
# GENERATE AI ITINERARY USING MCP
# ============================================================

@router.post("/{trip_id}/generate-itinerary")
async def generate_trip_itinerary(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Verify trip ownership.
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.user_id == current_user.id
    ).first()

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )

    # 2. Generate itinerary using the MCP-enabled service.
    try:
        itinerary_text = await generate_itinerary(
            destination=trip.destination,
            start_date=str(trip.start_date),
            end_date=str(trip.end_date),
            travelers=trip.travelers,
            budget=float(trip.budget),
        )

        if not itinerary_text or not itinerary_text.strip():
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="The AI returned an empty itinerary."
            )

    except HTTPException:
        raise

    except OpenAIError:
        logger.exception("OpenAI itinerary generation failed")

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI provider could not generate the itinerary."
        )

    except Exception:
        logger.exception("MCP itinerary generation failed")

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                "Itinerary generation failed. Check that the MCP "
                "server is running and inspect the backend logs."
            )
        )

    # 3. Create or update the saved itinerary.
    itinerary = db.query(Itinerary).filter(
        Itinerary.trip_id == trip.id
    ).first()

    if itinerary:
        itinerary.content = itinerary_text
    else:
        itinerary = Itinerary(
            trip_id=trip.id,
            content=itinerary_text
        )
        db.add(itinerary)

    # 4. Persist the itinerary in PostgreSQL.
    try:
        db.commit()
        db.refresh(itinerary)

    except Exception:
        db.rollback()
        logger.exception("Failed to save itinerary to PostgreSQL")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The itinerary was generated but could not be saved."
        )

    return {
        "message": "Itinerary generated successfully",
        "trip_id": trip.id,
        "itinerary_id": itinerary.id,
        "itinerary": itinerary.content
    }


# ============================================================
# GET SAVED ITINERARY
# ============================================================

@router.get("/{trip_id}/itinerary")
def get_saved_itinerary(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify ownership before returning itinerary data.
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.user_id == current_user.id
    ).first()

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )

    itinerary = db.query(Itinerary).filter(
        Itinerary.trip_id == trip.id
    ).first()

    if itinerary is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No itinerary generated for this trip yet"
        )

    return {
        "trip_id": trip.id,
        "itinerary_id": itinerary.id,
        "itinerary": itinerary.content
    }
