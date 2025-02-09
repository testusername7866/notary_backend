from fastapi import FastAPI, UploadFile, File
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import logging

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

# If Tesseract isn't in PATH, set it:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.get("/")  # Root route to check if backend is live
def root():
    return {"message": "Notary Backend is Live"}

@app.get("/health")  # Health check route
def health_check():
    return {"status": "ok"}

@app.post("/extract_text/")
async def extract_text(file: UploadFile = File(...)):
    try:
        logging.info(f"Received file: {file.filename}")
        file_bytes = await file.read()

        # Explicitly pass your Poppler path here:
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
