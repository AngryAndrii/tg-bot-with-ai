import os

from google import genai
from google.genai import types
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("GEMINI_API_KEY")

class Order(BaseModel):
    order_number: str
    date: str
    client_name: str

client = genai.Client(api_key=TOKEN)

async def extract_order(text):
    response = await client.aio.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"я даю тобі рядок {text} "
                 f"- тобі потрібно витягнути звідси поля номер замовлення (order_number), дата (date), та назва клієнта (client_name). "
                 f"Та поверни ці данні. Дату завжди виводь у вигляді '05 вересня 2023 р.'(без лапок) ",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Order,
        )
    )

    try:
        order = Order.model_validate_json(response.text)
        return order

    except Exception as e:
        print("Invalid Gemini response:", e)
        return None
