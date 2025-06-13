import os
import sys
import shutil
import logging
from pathlib import Path
from typing import Union

try:
    import pytesseract
except ImportError:
    pytesseract = None

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

def check_tesseract_installed():
    if pytesseract is None:
        raise ImportError("pytesseract is not installed. Please install it with 'pip install pytesseract'.")
    if shutil.which("tesseract") is None:
        raise EnvironmentError("Tesseract OCR is not installed or not in PATH. Please install it from https://github.com/tesseract-ocr/tesseract")

def extract_text_from_image(image_path: Union[str, Path]) -> str:
    if Image is None:
        raise ImportError("Pillow is not installed. Please install it with 'pip install pillow'.")
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

def extract_text_from_pdf(pdf_path: Union[str, Path]) -> str:
    if pdfplumber is None:
        raise ImportError("pdfplumber is not installed. Please install it with 'pip install pdfplumber'.")
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            else:
                # Fallback to OCR if page is scanned
                if fitz is None:
                    raise ImportError("PyMuPDF (fitz) is required for OCR on scanned PDFs. Please install it with 'pip install pymupdf'.")
                doc = fitz.open(pdf_path)
                for page_num in range(len(doc)):
                    pix = doc[page_num].get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text += pytesseract.image_to_string(img) + "\n"
                break  # Already processed all pages with fitz
    return text

def save_text(text: str, output_path: Path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

def process_file(file_path: Path, logger=None):
    try:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        if file_path.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
            text = extract_text_from_image(file_path)
        elif file_path.suffix.lower() == ".pdf":
            text = extract_text_from_pdf(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
        output_path = file_path.with_suffix(".txt")
        save_text(text, output_path)
        if logger:
            logger.info(f"Success: {file_path}")
        return True
    except Exception as e:
        if logger:
            logger.error(f"Failed: {file_path} - {e}")
        return False

def process_folder(folder_path: Path, logger=None, show_progress=True):
    files = [f for f in folder_path.iterdir() if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".pdf"]]
    iterator = tqdm(files, desc="Processing") if tqdm and show_progress else files
    for file_path in iterator:
        process_file(file_path, logger=logger)

def setup_logger(log_file: Path = None):
    logger = logging.getLogger("TextExtractor")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Text Extraction Tool: Extract text from images and PDFs.")
    parser.add_argument("input", type=str, help="Input file or folder path")
    parser.add_argument("--log", type=str, help="Optional log file path")
    parser.add_argument("--no-progress", action="store_true", help="Disable progress bar")
    args = parser.parse_args()

    check_tesseract_installed()
    input_path = Path(args.input)
    logger = setup_logger(args.log)

    if input_path.is_file():
        process_file(input_path, logger=logger)
    elif input_path.is_dir():
        process_folder(input_path, logger=logger, show_progress=not args.no_progress)
    else:
        logger.error(f"Input path not found: {input_path}")

if __name__ == "__main__":
    main()
