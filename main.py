from fastapi import FastAPI, UploadFile, File
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import os
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Change for security later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Set Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ✅ Set Poppler Path
POPPLER_PATH = r"C:\Poppler\poppler-24.08.0\Library\bin"

# ✅ Health check route
@app.get("/")
def root():
    return {"message": "Welcome to Notary Backend!"}

# ✅ Upload route (Handles PDF text extraction)
@app.post("/upload/")
async def extract_text(file: UploadFile = File(...)):
    try:
        # Read uploaded file
        file_bytes = await file.read()

        # ✅ Convert PDF to images using Poppler
        images = convert_from_bytes(file_bytes, poppler_path=POPPLER_PATH)

        if not images:
            return {"error": "PDF conversion failed, no images generated."}

        # ✅ Extract text from each image
        text = "\n".join([pytesseract.image_to_string(img) for img in images])

        return {"extracted_text": text}

    except Exception as e:
        return {"error": str(e)}
