import re

# IMPORT pytesseract, allowing use of 'OTC Tesseract' image-to-text processor
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

# IMPORT system-specific variables
import config


# PATH to OTC Tesseract ['..\Tesseract-OCR\tesseract']
pytesseract.pytesseract.tesseract_cmd = config.tesseract_install_path

if __name__ == "__main__":
    img_str = pytesseract.image_to_string(Image.open('src/img/salmon.jpg'))
    print(img_str)

"""test sublime git"""