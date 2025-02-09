from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import logging

app = FastAPI()

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://notary-frontend-inky.vercel.app"],  # Only allow frontend access
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# If Tesseract isn't in PATH, set it:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.get("/")
def health_check():
    return {"message": "Backend is running successfully!"}

@app.post("/extract_text/")
async def extract_text(file: UploadFile = File(...)):
    try:
        logging.info(f"Received file: {file.filename}")
        file_bytes = await file.read()

        # Convert PDF to images
        images = convert_from_bytes(
            file_bytes,
            poppler_path=r"C:\Poppler\poppler-24.08.0\Library\bin"
        )

        text = ""
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"

        return {"extracted_text": text}

    except Exception as e:
        logging.error(f"PDF conversion failed: {e}")
        return {"error": str(e)}
