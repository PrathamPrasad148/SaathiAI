from pathlib import Path

def read_text_from_image(image_path: Path) -> str:
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip() if text.strip() else "No text recognized in image."
    except ImportError:
        return f"OCR Engine (pytesseract) is not installed. Screenshot saved to {image_path.name}"
    except Exception as err:
        return f"OCR read error: {err}"
