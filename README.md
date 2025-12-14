# Text Extractor Tool

## Short Description

A Python-based tool that extracts text from image files (JPEG, PNG, etc.) and PDF documents (including scanned PDFs) using OCR and PDF parsing libraries. Extracted text is automatically saved as `.txt` files in the same directory as the source files.

## Why this project?

This project exists to solve the common problem of extracting text from various document formats - whether they are images, regular PDFs, or scanned PDFs. It provides a simple, unified interface for text extraction, eliminating the need to use different tools for different file types. The tool is particularly useful for digitizing printed documents, processing batches of files, and making text in images and scanned documents searchable and editable.

## Features

- Extracts text from multiple image formats (JPEG, PNG, etc.)
- Extracts text from PDF documents (both text-based and scanned)
- Automatic file type detection
- Batch processing support (single file or entire folders)
- GUI application with real-time progress tracking
- Command-line interface for automation and scripting
- Robust error handling
- Progress bar and detailed logging
- Automatic dependency installation via launcher script

## Requirements

### Operating System
- Linux (Ubuntu, Debian, Fedora, Arch)
- macOS
- Windows

### Programming Language/Runtime
- Python 3.7 or higher

### External Tools
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (must be installed and accessible in PATH)

### Python Libraries
- pytesseract
- Pillow
- pdfplumber
- tqdm
- PyMuPDF

## Installation

### Automatic Installation (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/Ravi-Wijerathne/Text_Extractor.git
cd Text_Extractor
```

2. Run the automated launcher script:
```bash
chmod +x run_text_extractor.sh
./run_text_extractor.sh
```

The script will automatically check and install all prerequisites and dependencies.

### Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/Ravi-Wijerathne/Text_Extractor.git
cd Text_Extractor
```

2. Install Python dependencies:
```bash
pip install pytesseract Pillow pdfplumber tqdm PyMuPDF
```

3. Install Tesseract OCR:
   - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
   - **Fedora**: `sudo dnf install tesseract`
   - **Arch Linux**: `sudo pacman -S tesseract`
   - **macOS**: `brew install tesseract`
   - **Windows**: Download from [GitHub](https://github.com/tesseract-ocr/tesseract)

## Usage

### Quick Start with Launcher Script

Run the automated launcher that handles all setup:

```bash
./run_text_extractor.sh
```

The script will:
- Check all prerequisites and dependencies
- Automatically install missing components
- Present a menu to choose between GUI or CLI mode
- Launch the selected tool

### GUI Application

Launch the graphical user interface:

```bash
python text_extractor_gui.py
```

GUI features:
- Easy file/folder selection with browse buttons
- Real-time progress tracking
- Detailed logging window
- Visual status updates
- Support for batch processing

### Command Line Interface

```bash
python text_extractor.py <input_path>
```

**Parameters:**
- `<input_path>`: Path to a file or folder containing images/PDFs

## Configuration

The tool uses default settings that work for most cases. Configuration options include:

- **Tesseract Path**: Ensure Tesseract OCR is installed and added to your system PATH
- **Output Format**: Extracted text is saved as `.txt` files with the same name as the source file
- **Output Location**: Text files are saved in the same directory as the source files

For advanced Tesseract OCR configuration (language packs, engine modes), you can modify the `text_extractor.py` file.

## Examples

### Extract text from a single image:
```bash
python text_extractor.py /path/to/image.jpg
```
Output: `/path/to/image.txt`

### Process all files in a folder:
```bash
python text_extractor.py /path/to/documents/
```
Output: Multiple `.txt` files in the same folder

### Using the GUI:
1. Launch: `python text_extractor_gui.py`
2. Click "Browse" to select a file or folder
3. Click "Extract Text"
4. Monitor progress in the logging window

## Project Structure

```
Text_Extractor/
├── LICENSE                    # MIT License
├── README.md                  # Project documentation
├── text_extractor.py          # Core CLI text extraction script
├── text_extractor_gui.py      # GUI application
├── run_text_extractor.sh      # Automated launcher script
└── __pycache__/               # Python bytecode cache
```

## Contributing

Contributions are welcome! If you'd like to contribute to this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

Please ensure your code follows Python best practices and includes appropriate error handling.

## Testing

Currently, the project uses manual testing. To test the tool:

1. Prepare test files (images and PDFs with known text content)
2. Run the extractor on these files
3. Verify the output `.txt` files contain the expected text

Automated testing suite is planned for future releases.

## Roadmap

- [ ] Add support for more image formats (TIFF, BMP, WebP)
- [ ] Implement automated test suite
- [ ] Add support for multiple OCR languages
- [ ] Improve GUI with drag-and-drop functionality
- [ ] Add option to merge multiple text outputs
- [ ] Docker containerization for easy deployment
- [ ] Add support for batch OCR optimization settings

## Known Issues

- Tesseract OCR accuracy depends on image quality and text clarity
- Very large PDF files may take longer to process
- Some scanned PDFs with complex layouts may require manual verification
- Unicode characters in filenames may cause issues on some systems

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
