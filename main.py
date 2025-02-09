from fastapi import FastAPI, UploadFile, File
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import logging
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin (update this for security later)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Set the correct path for Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)


# 🔹 **Health Check Route**
@app.get("/")
def root():
    return {"message": "Welcome to Notary Backend!"}


# 🔹 **Text Extraction Endpoint**
@app.post("/upload/")
async def extract_text(file: UploadFile = File(...)):
    try:
        logging.info(f"Received file: {file.filename}")
        file_bytes = await file.read()

        # Convert PDF to images
        images = convert_from_bytes(
            file_bytes,
            poppler_path=r"C:\Poppler\poppler-24.08.0\Library\bin"  # Ensure this path is correct
        )

        text = ""
        for img in images:
            extracted_text = pytesseract.image_to_string(img)
            text += extracted_text + "\n"

        return {"extracted_text": text}

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return {"error": str(e)}
