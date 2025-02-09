from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image

app = FastAPI()

# Enable CORS to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Change this to your frontend URL later)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend is working!"}

@app.post("/upload/")  # This ensures POST requests work
async def upload_file(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        images = convert_from_bytes(file_bytes)
        text = "".join(pytesseract.image_to_string(img) for img in images)
        return {"extracted_text": text}
    except Exception as e:
        return {"error": str(e)}
