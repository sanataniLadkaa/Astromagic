import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

API_KEY = "AIzaSyA55kGhMDzfy7GRXm4uDHr5yQaSSVcIFh4"
GENERATIVE_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, name: str = Form(...), birth_date: str = Form(...),birth_time: str=Form(...), birth_place: str = Form(...)):
    print("Received POST request to /predict endpoint")
    print(f"Name: {name}, Birth Date: {birth_date},Birth Time: {birth_time}, Birth Place: {birth_place}")

    test_question = f"My name is {name} and my birth date is {birth_date} and my birth time is {birth_time} and my birth place is {birth_place} based on my given details please tell my zodiac sign and give relationship, financial, health, and career advice and some recommendation in each separate paragraph"

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": test_question
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(GENERATIVE_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        print("Received response from external API:")
        print(result)
    else:
        result = f"Error: {response.text}"
        print(f"Error in external API call: {response.text}")

    print(f"Result: {result}")
    print("Rendering result.html template")  # Debugging statement
    return templates.TemplateResponse("result.html", {"request": request, "result": result})

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)