from fastapi import FastAPI, UploadFile, File
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set paths
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Poppler\poppler-24.08.0\Library\bin"

# ✅ Health check route
@app.get("/")
def root():
    return {"message": "Welcome to Notary Backend!"}

# ✅ Upload route (Make sure this exists)
@app.post("/upload/")
async def extract_text(file: UploadFile = File(...)):
    try:
        logging.info(f"Received file: {file.filename}")
        file_bytes = await file.read()

        # Convert PDF to images
        images = convert_from_bytes(file_bytes, poppler_path=POPPLER_PATH)

        text = ""
        for img in images:
            extracted_text = pytesseract.image_to_string(img)
            text += extracted_text + "\n"

        return {"extracted_text": text}

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return {"error": str(e)}
