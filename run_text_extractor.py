#!/usr/bin/env python3
"""
Text Extractor Tool - Automated Setup and Launch Script
This script checks dependencies, installs missing packages, and launches the tool.
Cross-platform equivalent of run_text_extractor.sh.
"""

import os
import sys
import shutil
import subprocess
import platform

# ─── Color helpers (ANSI codes, disabled on Windows without VT support) ───

def _supports_color():
    if os.environ.get("NO_COLOR"):
        return False
    if platform.system() == "Windows":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            # Enable ANSI on Windows 10+
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

_COLOR = _supports_color()

class _C:
    RED    = "\033[0;31m" if _COLOR else ""
    GREEN  = "\033[0;32m" if _COLOR else ""
    YELLOW = "\033[1;33m" if _COLOR else ""
    BLUE   = "\033[0;34m" if _COLOR else ""
    CYAN   = "\033[0;36m" if _COLOR else ""
    BOLD   = "\033[1m"    if _COLOR else ""
    NC     = "\033[0m"    if _COLOR else ""

def print_banner():
    print(f"{_C.CYAN}{_C.BOLD}")
    print("╔════════════════════════════════════════════╗")
    print("║      TEXT EXTRACTOR TOOL - LAUNCHER        ║")
    print("║    Extract text from PDFs and Images       ║")
    print("╚════════════════════════════════════════════╝")
    print(f"{_C.NC}")

def print_section(msg):  print(f"\n{_C.BOLD}{_C.BLUE}═══ {msg} ═══{_C.NC}")
def print_success(msg):  print(f"{_C.GREEN}✓ {msg}{_C.NC}")
def print_error(msg):    print(f"{_C.RED}✗ {msg}{_C.NC}")
def print_warning(msg):  print(f"{_C.YELLOW}⚠ {msg}{_C.NC}")
def print_info(msg):     print(f"{_C.CYAN}ℹ {msg}{_C.NC}")

# ─── Paths ────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR   = os.path.join(SCRIPT_DIR, "venv")

# ─── Dependency checks ───────────────────────────────────────────────────

def check_python():
    """Verify the running Python meets the minimum version requirement."""
    print_section("Checking Python Installation")
    ver = sys.version.split()[0]
    print_success(f"Python is installed: {ver}")

    major, minor = sys.version_info[:2]
    if major >= 3 and minor >= 7:
        print_success("Python version meets requirements (3.7+)")
        return True
    else:
        print_warning("Python version is less than 3.7, but will try to continue")
        return True


def check_pip():
    """Check that pip is available."""
    print_section("Checking pip Installation")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print_success("pip is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("pip is not available for the current Python interpreter")
        print_info("Install pip: https://pip.pypa.io/en/stable/installation/")
        return False


def check_tesseract():
    """Check (and optionally install) Tesseract OCR."""
    print_section("Checking Tesseract OCR Installation")

    tess = shutil.which("tesseract")
    if tess:
        try:
            ver = subprocess.check_output(
                ["tesseract", "--version"], stderr=subprocess.STDOUT
            ).decode().splitlines()[0]
            print_success(f"Tesseract OCR is installed: {ver}")
        except Exception:
            print_success("Tesseract OCR is installed")
        return True

    print_warning("Tesseract OCR is not installed")

    system = platform.system()
    installed = False

    if system == "Linux":
        pkg_managers = [
            (["apt-get", "update"], ["apt-get", "install", "-y", "tesseract-ocr"]),
            (None,                  ["dnf", "install", "-y", "tesseract"]),
            (None,                  ["yum", "install", "-y", "tesseract"]),
            (None,                  ["pacman", "-S", "--noconfirm", "tesseract"]),
        ]
        for update_cmd, install_cmd in pkg_managers:
            if shutil.which(install_cmd[0]):
                print_info(f"Installing via {install_cmd[0]}...")
                try:
                    if update_cmd:
                        subprocess.check_call(["sudo"] + update_cmd,
                                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    subprocess.check_call(["sudo"] + install_cmd)
                    installed = True
                except Exception:
                    pass
                break
    elif system == "Darwin":
        if shutil.which("brew"):
            print_info("Installing via Homebrew...")
            try:
                subprocess.check_call(["brew", "install", "tesseract"])
                installed = True
            except Exception:
                pass

    if installed and shutil.which("tesseract"):
        print_success("Tesseract OCR installed successfully")
        return True

    print_error("Could not install Tesseract automatically")
    print_info("Please install Tesseract manually:")
    print_info("  Ubuntu/Debian : sudo apt-get install tesseract-ocr")
    print_info("  Fedora        : sudo dnf install tesseract")
    print_info("  Arch          : sudo pacman -S tesseract")
    print_info("  macOS         : brew install tesseract")
    print_info("  Windows       : https://github.com/tesseract-ocr/tesseract")
    return False


# ─── Virtual-environment & package management ─────────────────────────────

def _python_cmd():
    """Return the Python executable to use (venv-aware)."""
    if os.path.isdir(VENV_DIR):
        if platform.system() == "Windows":
            candidate = os.path.join(VENV_DIR, "Scripts", "python.exe")
        else:
            candidate = os.path.join(VENV_DIR, "bin", "python")
        if os.path.isfile(candidate):
            return candidate
    return sys.executable


def _pip_install(packages: list[str], use_user: bool = False) -> bool:
    """Run pip install for *packages*. Returns True on success."""
    cmd = [_python_cmd(), "-m", "pip", "install"]
    if use_user:
        cmd.append("--user")
    cmd.extend(packages)
    try:
        subprocess.check_call(cmd)
        return True
    except subprocess.CalledProcessError:
        return False


def _create_venv() -> bool:
    print_section("Setting Up Virtual Environment")
    if os.path.isdir(VENV_DIR):
        print_success("Virtual environment already exists")
        return True
    print_info("Creating virtual environment...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
        print_success("Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to create virtual environment")
        print_info("Make sure python3-venv is installed: sudo apt-get install python3-venv")
        return False


def _check_package(package: str) -> bool:
    """Return True if *package* is importable by the target Python."""
    try:
        subprocess.check_call(
            [_python_cmd(), "-c", f"import {package}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_python_packages() -> bool:
    """Check required packages and install any that are missing."""
    print_section("Checking Python Dependencies")

    required = {
        "pytesseract": "pytesseract",
        "PIL":         "Pillow",
        "pdfplumber":  "pdfplumber",
        "tqdm":        "tqdm",
        "fitz":        "PyMuPDF",
    }

    missing_pip: list[str] = []
    for import_name, pip_name in required.items():
        if _check_package(import_name):
            print_success(f"{import_name} is installed")
        else:
            print_warning(f"{import_name} is not installed")
            missing_pip.append(pip_name)

    if not missing_pip:
        print_success("All Python packages are already installed")
        return True

    print_info(f"Installing missing Python packages: {', '.join(missing_pip)}")

    # Try --user install first
    if _pip_install(missing_pip, use_user=True):
        print_success("All Python packages installed successfully")
        return True

    # Fall back to a virtual-environment install
    print_warning("System Python is externally-managed, using virtual environment...")
    if not _create_venv():
        return False
    if _pip_install(missing_pip, use_user=False):
        print_success("All Python packages installed successfully")
        return True

    print_error("Failed to install packages")
    return False


# ─── Menu / launch ────────────────────────────────────────────────────────

def show_menu():
    print_section("Select Mode")
    print()
    print(f"{_C.BOLD}1){_C.NC} GUI Mode (Graphical User Interface)")
    print(f"{_C.BOLD}2){_C.NC} CLI Mode (Command Line Interface)")
    print(f"{_C.BOLD}3){_C.NC} Exit")
    print()


def launch_gui():
    print_section("Launching GUI Mode")
    print_info("Starting Text Extractor GUI...")
    os.chdir(SCRIPT_DIR)
    subprocess.call([_python_cmd(), os.path.join(SCRIPT_DIR, "text_extractor_gui.py")])


def launch_cli():
    print_section("Launching CLI Mode")
    print()
    try:
        input_path = input(f"{_C.CYAN}Enter file or folder path: {_C.NC}").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return

    if not input_path:
        print_error("No path provided")
        return

    if not os.path.exists(input_path):
        print_error(f"Path does not exist: {input_path}")
        return

    print_info(f"Processing: {input_path}")
    os.chdir(SCRIPT_DIR)
    subprocess.call([_python_cmd(), os.path.join(SCRIPT_DIR, "text_extractor.py"), input_path])


# ─── Main ─────────────────────────────────────────────────────────────────

def main():
    # Clear screen (cross-platform)
    os.system("cls" if platform.system() == "Windows" else "clear")

    print_banner()
    print_info("Checking system requirements...")
    print()

    checks_passed = True

    if not check_python():
        checks_passed = False
    if not check_pip():
        checks_passed = False
    if not check_tesseract():
        checks_passed = False
    if not install_python_packages():
        checks_passed = False

    if not checks_passed:
        print()
        print_error("Some dependencies are missing. Please install them manually and run this script again.")
        sys.exit(1)

    print()
    print_success("All dependencies are installed!")

    # Main loop
    while True:
        print()
        show_menu()
        try:
            choice = input(f"{_C.CYAN}Enter your choice [1-3]: {_C.NC}").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print_info("Exiting... Goodbye!")
            break

        if choice == "1":
            launch_gui()
            print()
            print_info("GUI closed. Returning to menu...")
        elif choice == "2":
            launch_cli()
            print()
            print_info("Processing complete. Returning to menu...")
        elif choice == "3":
            print()
            print_info("Exiting... Goodbye!")
            break
        else:
            print_error("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
