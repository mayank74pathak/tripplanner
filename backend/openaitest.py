import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL", "gpt-5-mini")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing from .env")

client = OpenAI(api_key=api_key)

try:
    response = client.responses.create(
        model=model,
        input="Reply with exactly: OpenAI connection successful."
    )

    print("SUCCESS: API key and model are working.")
    print("Response:", response.output_text)

except Exception as e:
    print("API test failed.")
    print("Error type:", type(e).__name__)
    print("Error:", str(e))