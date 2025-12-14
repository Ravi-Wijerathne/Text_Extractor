#!/bin/bash

# Text Extractor Tool - Automated Setup and Launch Script
# This script checks dependencies, installs missing packages, and launches the tool

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

# Banner
print_banner() {
    echo -e "${CYAN}${BOLD}"
    echo "╔════════════════════════════════════════════╗"
    echo "║      TEXT EXTRACTOR TOOL - LAUNCHER        ║"
    echo "║    Extract text from PDFs and Images       ║"
    echo "╚════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Print section header
print_section() {
    echo -e "\n${BOLD}${BLUE}═══ $1 ═══${NC}"
}

# Print success message
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Print error message
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Print warning message
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Print info message
print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python installation
check_python() {
    print_section "Checking Python Installation"
    
    if command_exists python3; then
        PYTHON_CMD="python3"
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_success "Python 3 is installed: $PYTHON_VERSION"
        
        # Check if version is 3.7+
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        
        if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 7 ]; then
            print_success "Python version meets requirements (3.7+)"
            return 0
        else
            print_warning "Python version is less than 3.7, but will try to continue"
            return 0
        fi
    elif command_exists python; then
        PYTHON_CMD="python"
        PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
        print_success "Python is installed: $PYTHON_VERSION"
        return 0
    else
        print_error "Python 3 is not installed"
        print_info "Please install Python 3.7+ from https://www.python.org/"
        print_info "On Ubuntu/Debian: sudo apt-get install python3 python3-pip"
        print_info "On Fedora: sudo dnf install python3 python3-pip"
        print_info "On macOS: brew install python3"
        return 1
    fi
}

# Check pip installation
check_pip() {
    print_section "Checking pip Installation"
    
    if command_exists pip3; then
        PIP_CMD="pip3"
        print_success "pip3 is installed"
        return 0
    elif command_exists pip; then
        PIP_CMD="pip"
        print_success "pip is installed"
        return 0
    else
        print_warning "pip is not installed. Attempting to install..."
        
        if command_exists apt-get; then
            sudo apt-get update && sudo apt-get install -y python3-pip
        elif command_exists dnf; then
            sudo dnf install -y python3-pip
        elif command_exists yum; then
            sudo yum install -y python3-pip
        elif command_exists brew; then
            brew install python3
        else
            print_error "Could not install pip automatically"
            print_info "Please install pip manually: curl https://bootstrap.pypa.io/get-pip.py | python3"
            return 1
        fi
        
        if command_exists pip3; then
            PIP_CMD="pip3"
            print_success "pip3 installed successfully"
            return 0
        else
            return 1
        fi
    fi
}

# Check Tesseract OCR installation
check_tesseract() {
    print_section "Checking Tesseract OCR Installation"
    
    if command_exists tesseract; then
        TESSERACT_VERSION=$(tesseract --version 2>&1 | head -n1)
        print_success "Tesseract OCR is installed: $TESSERACT_VERSION"
        return 0
    else
        print_warning "Tesseract OCR is not installed"
        print_info "Attempting to install Tesseract OCR..."
        
        if command_exists apt-get; then
            print_info "Installing via apt-get..."
            sudo apt-get update && sudo apt-get install -y tesseract-ocr
        elif command_exists dnf; then
            print_info "Installing via dnf..."
            sudo dnf install -y tesseract
        elif command_exists yum; then
            print_info "Installing via yum..."
            sudo yum install -y tesseract
        elif command_exists brew; then
            print_info "Installing via Homebrew..."
            brew install tesseract
        elif command_exists pacman; then
            print_info "Installing via pacman..."
            sudo pacman -S --noconfirm tesseract
        else
            print_error "Could not install Tesseract automatically"
            print_info "Please install Tesseract manually:"
            print_info "  Ubuntu/Debian: sudo apt-get install tesseract-ocr"
            print_info "  Fedora: sudo dnf install tesseract"
            print_info "  Arch: sudo pacman -S tesseract"
            print_info "  macOS: brew install tesseract"
            print_info "  Or visit: https://github.com/tesseract-ocr/tesseract"
            return 1
        fi
        
        if command_exists tesseract; then
            print_success "Tesseract OCR installed successfully"
            return 0
        else
            print_error "Failed to install Tesseract OCR"
            return 1
        fi
    fi
}

# Check Python package installation
check_python_package() {
    local package=$1
    $PYTHON_CMD -c "import $package" 2>/dev/null
    return $?
}

# Create virtual environment
create_venv() {
    print_section "Setting Up Virtual Environment"
    
    if [ -d "$VENV_DIR" ]; then
        print_success "Virtual environment already exists"
        return 0
    fi
    
    print_info "Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    
    if [ $? -eq 0 ]; then
        print_success "Virtual environment created successfully"
        return 0
    else
        print_error "Failed to create virtual environment"
        print_info "Make sure python3-venv is installed: sudo apt-get install python3-venv"
        return 1
    fi
}

# Activate virtual environment
activate_venv() {
    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
        PYTHON_CMD="$VENV_DIR/bin/python"
        PIP_CMD="$VENV_DIR/bin/pip"
        print_success "Virtual environment activated"
        return 0
    else
        print_error "Virtual environment not found"
        return 1
    fi
}

# Install Python packages
install_python_packages() {
    print_section "Checking Python Dependencies"
    
    REQUIRED_PACKAGES=("pytesseract" "PIL" "pdfplumber" "tqdm" "fitz")
    INSTALL_PACKAGES=()
    
    # Check each package
    for package in "${REQUIRED_PACKAGES[@]}"; do
        if check_python_package "$package"; then
            print_success "$package is installed"
        else
            print_warning "$package is not installed"
            if [ "$package" == "PIL" ]; then
                INSTALL_PACKAGES+=("Pillow")
            elif [ "$package" == "fitz" ]; then
                INSTALL_PACKAGES+=("PyMuPDF")
            else
                INSTALL_PACKAGES+=("$package")
            fi
        fi
    done
    
    # Install missing packages
    if [ ${#INSTALL_PACKAGES[@]} -gt 0 ]; then
        print_info "Installing missing Python packages: ${INSTALL_PACKAGES[*]}"
        
        # Try installing with --user flag first
        $PIP_CMD install --user "${INSTALL_PACKAGES[@]}" 2>/dev/null
        
        # If that fails (externally-managed environment), use venv
        if [ $? -ne 0 ]; then
            print_warning "System Python is externally-managed, using virtual environment..."
            
            # Create and activate venv
            if ! create_venv; then
                return 1
            fi
            
            if ! activate_venv; then
                return 1
            fi
            
            # Install packages in venv
            print_info "Installing packages in virtual environment..."
            $PIP_CMD install "${INSTALL_PACKAGES[@]}"
            
            if [ $? -ne 0 ]; then
                print_error "Failed to install packages in virtual environment"
                return 1
            fi
        fi
        
        print_success "All Python packages installed successfully"
        return 0
    else
        print_success "All Python packages are already installed"
        return 0
    fi
}

# Show menu and get user choice
show_menu() {
    print_section "Select Mode"
    echo ""
    echo -e "${BOLD}1)${NC} GUI Mode (Graphical User Interface)"
    echo -e "${BOLD}2)${NC} CLI Mode (Command Line Interface)"
    echo -e "${BOLD}3)${NC} Exit"
    echo ""
    echo -ne "${CYAN}Enter your choice [1-3]: ${NC}"
}

# Launch GUI mode
launch_gui() {
    print_section "Launching GUI Mode"
    print_info "Starting Text Extractor GUI..."
    cd "$SCRIPT_DIR"
    
    # Use venv python if it exists
    if [ -f "$VENV_DIR/bin/python" ]; then
        "$VENV_DIR/bin/python" text_extractor_gui.py
    else
        $PYTHON_CMD text_extractor_gui.py
    fi
}

# Launch CLI mode
launch_cli() {
    print_section "Launching CLI Mode"
    echo ""
    echo -ne "${CYAN}Enter file or folder path: ${NC}"
    read -r input_path
    
    if [ -z "$input_path" ]; then
        print_error "No path provided"
        return 1
    fi
    
    if [ ! -e "$input_path" ]; then
        print_error "Path does not exist: $input_path"
        return 1
    fi
    
    print_info "Processing: $input_path"
    cd "$SCRIPT_DIR"
    
    # Use venv python if it exists
    if [ -f "$VENV_DIR/bin/python" ]; then
        "$VENV_DIR/bin/python" text_extractor.py "$input_path"
    else
        $PYTHON_CMD text_extractor.py "$input_path"
    fi
}

# Main function
main() {
    clear
    print_banner
    
    # Check all dependencies
    print_info "Checking system requirements..."
    echo ""
    
    CHECKS_PASSED=true
    
    if ! check_python; then
        CHECKS_PASSED=false
    fi
    
    if ! check_pip; then
        CHECKS_PASSED=false
    fi
    
    if ! check_tesseract; then
        CHECKS_PASSED=false
    fi
    
    if ! install_python_packages; then
        CHECKS_PASSED=false
    fi
    
    if [ "$CHECKS_PASSED" = false ]; then
        echo ""
        print_error "Some dependencies are missing. Please install them manually and run this script again."
        exit 1
    fi
    
    echo ""
    print_success "All dependencies are installed!"
    
    # Main loop
    while true; do
        echo ""
        show_menu
        read -r choice
        
        case $choice in
            1)
                launch_gui
                echo ""
                print_info "GUI closed. Returning to menu..."
                ;;
            2)
                launch_cli
                echo ""
                print_info "Processing complete. Returning to menu..."
                ;;
            3)
                echo ""
                print_info "Exiting... Goodbye!"
                exit 0
                ;;
            *)
                print_error "Invalid choice. Please enter 1, 2, or 3."
                ;;
        esac
    done
}

# Run main function
main
