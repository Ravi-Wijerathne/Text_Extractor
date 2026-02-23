# Text Extractor Tool

A Python-based tool that extracts text from images (JPEG, PNG, BMP, TIFF) and PDFs (including scanned) using OCR. Extracted text is saved as `.txt` files alongside the source files.

## Setup

### Prerequisites

- Python 3.7+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed and in PATH

### Install

```bash
git clone https://github.com/Ravi-Wijerathne/Text_Extractor.git
cd Text_Extractor
pip install pytesseract Pillow pdfplumber tqdm PyMuPDF
```

**Install Tesseract OCR:**

| OS | Command |
|---|---|
| Ubuntu/Debian | `sudo apt-get install tesseract-ocr` |
| Fedora | `sudo dnf install tesseract` |
| Arch | `sudo pacman -S tesseract` |
| macOS | `brew install tesseract` |
| Windows | [Download installer](https://github.com/tesseract-ocr/tesseract) |

> On Linux/macOS, you can alternatively run `./run_text_extractor.sh` to auto-install all dependencies and launch the tool.

> **Cross-platform launcher:** You can also run `python run_text_extractor.py` on any platform (Windows, macOS, Linux). It performs the same dependency checks, optional virtual-environment setup, and interactive menu as the shell script — no Bash required.

## Usage

**CLI** — process a single file or an entire folder:

```bash
python text_extractor.py <file_or_folder>
```

**GUI** — launch the graphical interface:

```bash
python text_extractor_gui.py
```

## License

[MIT](LICENSE)

## FAQ

**Q: What image formats are supported?**  
A: The tool supports common formats like JPEG, PNG, and other formats supported by Pillow (PIL).

**Q: Can I extract text from scanned PDFs?**  
A: Yes, the tool automatically detects scanned PDFs and applies OCR.

**Q: Where are the output files saved?**  
A: Text files are saved in the same directory as the source files with a `.txt` extension.

**Q: Do I need to install Tesseract separately?**  
A: Yes, Tesseract OCR must be installed on your system. The launcher script can help with this.

**Q: Can I process multiple files at once?**  
A: Yes, simply provide a folder path instead of a file path.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Authors

- **Ravi Wijerathne** - [GitHub Profile](https://github.com/Ravi-Wijerathne)

---

*For issues, questions, or suggestions, please open an issue on GitHub.*
