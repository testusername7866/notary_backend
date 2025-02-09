from fastapi import FastAPI, UploadFile, File
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Set the Poppler path explicitly
POPPLER_PATH = r"C:\Poppler\poppler-24.08.0\Library\bin"

@app.post("/extract_text/")
async def extract_text(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()

        # Convert PDF to images using Poppler
        images = convert_from_bytes(file_bytes, poppler_path=POPPLER_PATH)

        text = ""
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"

        return {"extracted_text": text}

    except Exception as e:
        return {"error": str(e)}
