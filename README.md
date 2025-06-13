# Text Extractor Tool

## Overview

This Python script extracts text from image files (JPEG, PNG, etc.) and PDF documents (including scanned PDFs) using OCR and PDF parsing libraries. It saves the extracted text as a `.txt` file with the same filename in the same directory as the original file. The tool can process individual files or all files in a folder.

## Features

- Extracts text from images and PDFs (including scanned PDFs)
- Automatically detects file type
- Processes single files or all files in a folder
- Handles errors (file not found, unreadable file, missing OCR engine)
- Saves output as `.txt` in the same directory
- Logging and progress bar support

## Requirements

- Python 3.7+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (must be installed and accessible in PATH)
- Python packages:
  - pytesseract
  - Pillow
  - pdfplumber
  - tqdm

Install dependencies with:

```
pip install pytesseract Pillow pdfplumber tqdm
```

## Usage

### Command Line

```
python text_extractor.py <input_path>
```

- `<input_path>`: Path to a file or folder containing images/PDFs.

### Example

```
python text_extractor.py ./documents
```

## Notes

- For scanned PDFs, OCR is automatically applied.
- Output `.txt` files are saved next to the originals.
- Ensure Tesseract is installed and added to your system PATH.

## Optional Enhancements

- Logging for each file's success/failure
- Progress bar with `tqdm`
- Simple GUI (future work)

## License

MIT License
