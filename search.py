import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def search_from_query(query):
    prompt = f"Return concise information on {query}"

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {
                "role":"system", "content": "You are an empathetic well-being coach who provides uplifting quotes"},
            {   "role":"user", "content":prompt}
            ],
            temperature = 0.8,
            max_tokens = 50
    )
    return response.choices[0].message.content.strip()

def image_from_query(query):
    response = client.images.generate(
        model = "gpt-image-1",
        prompt= f"A calming, and inspiring image based on {query}",
        size = "1024x1024"
    )
    return response.data[0].url