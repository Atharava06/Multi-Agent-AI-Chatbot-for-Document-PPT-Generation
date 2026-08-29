import pytesseract
from PIL import Image
import pdfplumber
import io

class OCRService:
    def extract_text_from_image(self, image_path: str) -> str:
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            return f"OCR Error (Image): {str(e)}"
            
    def extract_text_from_scanned_pdf(self, pdf_path: str) -> str:
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    im = page.to_image(resolution=300)
                    pil_image = im.original
                    text += pytesseract.image_to_string(pil_image) + "\n"
            return text
        except Exception as e:
            return f"OCR Error (PDF): {str(e)}"

ocr_service = OCRService()
