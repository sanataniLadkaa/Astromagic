import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Replace with your own API key
API_KEY = "AIzaSyAPCWYCtTB_TivgGt9yNaYXXivxVFjijTw"
GENERATIVE_API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page (index.html)"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request, 
    name: str = Form(...), 
    birth_date: str = Form(...), 
    birth_time: str = Form(...), 
    birth_place: str = Form(...)
):
    """Handle the prediction request"""
    # Construct the input query for the API
    test_question = (
        f"My name is {name} and my birth date is {birth_date}, "
        f"my birth time is {birth_time}, and my birth place is {birth_place}. "
        f"Please tell me my zodiac sign and provide relationship, financial, health, "
        f"and career advice, along with recommendations in separate paragraphs."
    )

    # Define the payload for the API request
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": test_question}
                ]
            }
        ]
    }


    # API request headers
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Send the request to the external API
        response = requests.post(GENERATIVE_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        # Debug: Print the full API response
        print("API Response:", response.json())

        # Extract the result text
        result = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response received.")
    except Exception as e:
        result = f"Error: {str(e)}"


    # Render the result.html template with the response
    return templates.TemplateResponse("result.html", {"request": request, "result": result})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
