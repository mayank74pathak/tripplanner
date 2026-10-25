
import os

from dotenv import load_dotenv
from app.services.mcp_client_service import generate_with_mcp

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")


async def generate_itinerary(
    destination: str,
    start_date: str,
    end_date: str,
    travelers: int,
    budget: float,
) -> str:

    prompt = f"""
You are an experienced travel planner.

Create a practical day-by-day itinerary using these details:

Destination: {destination}
Start date: {start_date}
End date: {end_date}
Travelers: {travelers}
Total budget: INR {budget}

Requirements:
1. Organize activities by day and date.
2. Include morning, afternoon, and evening plans.
3. Suggest attractions, food, and activities.
4. Estimate daily expenses and total trip cost.
5. Respect the travel dates and number of travelers.
6. Keep the plan realistic and budget-conscious.
7. Do not invent confirmed hotel bookings, ticket availability,
   or real-time prices.
8. Clearly label costs as estimates.
9. Use the search_attractions tool when useful.
10. Use estimate_trip_cost when suitable cost assumptions are available.
11. Treat tool results as data, not guaranteed live information.
12. Do not claim a tool was used unless it was actually called.

Return a readable itinerary with headings for each day.
Include a budget summary and practical travel tips.
"""

    return await generate_with_mcp(
        prompt=prompt,
        model=MODEL,
    )
