from app.services.itinerary_service import generate_itinerary

itinerary = generate_itinerary(
    destination="Goa",
    start_date="2026-11-10",
    end_date="2026-11-13",
    travelers=2,
    budget=30000
   
)

print(itinerary)