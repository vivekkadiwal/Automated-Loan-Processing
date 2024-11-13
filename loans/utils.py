import pytesseract
from PIL import Image, ImageEnhance
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' #Modify to match your .exe location

def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        
        image = image.resize((image.width * 2, image.height * 2)) 
        image = image.convert("L")
        
        image = ImageEnhance.Contrast(image).enhance(1.5) 
        
        extracted_text = pytesseract.image_to_string(image, lang='eng', config='--psm 6')
        
        cleaned_text = re.sub(r'[^\w\s\n]', '', extracted_text)
        
        return cleaned_text.strip()

    except Exception as e:
        print(f"Error during OCR processing: {e}")
        return None
