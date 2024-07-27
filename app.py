from fastapi import FastAPI, Form, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Configure Generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to process input image for AI model
def input_image_setup(file: UploadFile):
    file.file.seek(0)
    image_parts = [{"mime_type": file.content_type, "data": file.file.read()}]
    return image_parts

# Function to retrieve response from Generative AI model
def get_gemini_response(input_text, image_data, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input_text, image_data[0], prompt])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Function to calculate BMI
def calculate_bmi(weight: float, height: float) -> float:
    height_meters = height / 100
    bmi = weight / (height_meters ** 2)
    return round(bmi, 2)

# Function to calculate ideal BMI
def calculate_ideal_bmi(age: int) -> float:
    if age <= 18:
        return 21.0
    elif 18 < age <= 29:
        return 22.0
    elif 30 <= age <= 39:
        return 23.0
    else:
        return 24.0

# FastAPI route to serve the index.html template
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# FastAPI route to handle form submission and process calculations
@app.post("/calculate/", response_model=dict)
async def calculate(name: str = Form(...), input: str = Form(...), age: int = Form(...), weight: float = Form(...), height: float = Form(...), meal_type: str = Form(...), file: UploadFile = File(...)):
    try:
        # Process uploaded image
        image_data = input_image_setup(file)
        
        # Calculate BMI and ideal BMI
        bmi = calculate_bmi(weight, height)
        ideal_bmi = calculate_ideal_bmi(age)

        # Prepare input prompt for AI model
        input_prompt = f"""
            Assess the meal for {meal_type}:
            - Caloric content and suitability for BMI of {bmi}.
            - Suggest alternatives if necessary.
        """
        
        # Get response from Generative AI model
        response = get_gemini_response(input, image_data, input_prompt)

        # Return response data
        return {"message": "Success", "response": response, "bmi": bmi, "ideal_bmi": ideal_bmi}
    except Exception as e:
        return {"message": "Error processing request.", "error": str(e)}
