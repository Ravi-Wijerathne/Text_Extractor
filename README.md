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
  - PyMuPDF

### Automatic Installation

The easiest way to install all dependencies is to run:

```bash
./run_text_extractor.sh
```

### Manual Installation

Install dependencies with:

```
pip install pytesseract Pillow pdfplumber tqdm PyMuPDF
```

Install Tesseract OCR:
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
- **Fedora**: `sudo dnf install tesseract`
- **Arch Linux**: `sudo pacman -S tesseract`
- **macOS**: `brew install tesseract`
- **Windows**: Download from [GitHub](https://github.com/tesseract-ocr/tesseract)

## Usage

### Quick Start (Recommended)

Run the automated launcher script that handles all setup:

```bash
./run_text_extractor.sh
```

This script will:
- ✓ Check all prerequisites and dependencies
- ✓ Automatically install missing components
- ✓ Present a menu to choose between GUI or CLI mode
- ✓ Launch the selected tool

### Manual Usage

#### GUI Application

Run the graphical user interface:

```
python text_extractor_gui.py
```

Features:
- Easy file/folder selection with browse buttons
- Real-time progress tracking
- Detailed logging window
- Visual status updates
- Support for batch processing

#### Command Line

```
python text_extractor.py <input_path>
```

- `<input_path>`: Path to a file or folder containing images/PDFs.

#### Example

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
