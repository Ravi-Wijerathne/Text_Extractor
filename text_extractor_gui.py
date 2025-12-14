import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
from pathlib import Path
from text_extractor import (
    extract_text_from_image,
    extract_text_from_pdf,
    save_text,
    check_tesseract_installed,
    process_file,
    process_folder
)


class TextExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Extractor Tool")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.input_path = tk.StringVar()
        self.processing = False
        
        # Check Tesseract on startup
        self.check_dependencies()
        
        # Create UI
        self.create_widgets()
        
    def check_dependencies(self):
        try:
            check_tesseract_installed()
        except Exception as e:
            messagebox.showerror("Dependency Error", str(e))
            self.root.after(100, self.root.destroy)
    
    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X, side=tk.TOP)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="📄 Text Extractor Tool",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title_label.pack(pady=15)
        
        # Main content frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input selection frame
        input_frame = tk.LabelFrame(main_frame, text="Input Selection", font=("Arial", 10, "bold"), padx=10, pady=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Path entry
        path_frame = tk.Frame(input_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(path_frame, text="Path:", width=8, anchor="w").pack(side=tk.LEFT)
        
        path_entry = tk.Entry(path_frame, textvariable=self.input_path, font=("Arial", 10))
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Buttons frame
        button_frame = tk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(
            button_frame,
            text="📁 Select File",
            command=self.select_file,
            bg="#3498db",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="📂 Select Folder",
            command=self.select_folder,
            bg="#3498db",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        # Process button
        self.process_btn = tk.Button(
            button_frame,
            text="▶️ Process",
            command=self.process_input,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5,
            cursor="hand2"
        )
        self.process_btn.pack(side=tk.LEFT, padx=20)
        
        # Progress frame
        progress_frame = tk.LabelFrame(main_frame, text="Progress", font=("Arial", 10, "bold"), padx=10, pady=10)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.status_label = tk.Label(progress_frame, text="Ready", font=("Arial", 9), anchor="w")
        self.status_label.pack(fill=tk.X)
        
        # Output/Log frame
        log_frame = tk.LabelFrame(main_frame, text="Log", font=("Arial", 10, "bold"), padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            height=15,
            bg="#f8f9fa",
            fg="#212529"
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Clear log button
        tk.Button(
            log_frame,
            text="Clear Log",
            command=self.clear_log,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 9),
            padx=10,
            pady=3,
            cursor="hand2"
        ).pack(pady=(5, 0))
        
        # Info frame
        info_frame = tk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        info_text = "Supported formats: PDF, JPG, JPEG, PNG, BMP, TIFF | Output: .txt files in the same directory"
        tk.Label(info_frame, text=info_text, font=("Arial", 8), fg="#6c757d").pack()
    
    def select_file(self):
        filename = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[
                ("All Supported", "*.pdf *.jpg *.jpeg *.png *.bmp *.tiff"),
                ("PDF files", "*.pdf"),
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.input_path.set(filename)
            self.log(f"Selected file: {filename}")
    
    def select_folder(self):
        folder = filedialog.askdirectory(title="Select a folder")
        if folder:
            self.input_path.set(folder)
            self.log(f"Selected folder: {folder}")
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
    
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def process_input(self):
        if self.processing:
            messagebox.showwarning("Processing", "Already processing. Please wait.")
            return
        
        path = self.input_path.get()
        if not path:
            messagebox.showwarning("No Input", "Please select a file or folder first.")
            return
        
        input_path = Path(path)
        if not input_path.exists():
            messagebox.showerror("Error", f"Path does not exist: {path}")
            return
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self.process_thread, args=(input_path,))
        thread.daemon = True
        thread.start()
    
    def process_thread(self, input_path):
        self.processing = True
        self.process_btn.config(state=tk.DISABLED)
        self.progress_bar.start(10)
        
        try:
            if input_path.is_file():
                self.update_status(f"Processing file: {input_path.name}")
                self.log(f"\n{'='*60}")
                self.log(f"Processing file: {input_path}")
                success = self.process_single_file(input_path)
                if success:
                    self.log(f"✓ Success: Extracted text saved to {input_path.with_suffix('.txt')}")
                    self.update_status("Completed successfully!")
                else:
                    self.update_status("Processing failed. Check log for details.")
                    
            elif input_path.is_dir():
                self.update_status(f"Processing folder: {input_path.name}")
                self.log(f"\n{'='*60}")
                self.log(f"Processing folder: {input_path}")
                self.process_folder_files(input_path)
                self.update_status("Folder processing completed!")
            
            messagebox.showinfo("Complete", "Processing completed! Check the log for details.")
            
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            self.update_status("Error occurred during processing")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            self.progress_bar.stop()
            self.processing = False
            self.process_btn.config(state=tk.NORMAL)
    
    def process_single_file(self, file_path):
        try:
            if file_path.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
                text = extract_text_from_image(file_path)
            elif file_path.suffix.lower() == ".pdf":
                text = extract_text_from_pdf(file_path)
            else:
                self.log(f"✗ Unsupported file type: {file_path.suffix}")
                return False
            
            output_path = file_path.with_suffix(".txt")
            save_text(text, output_path)
            return True
            
        except Exception as e:
            self.log(f"✗ Failed: {file_path.name} - {str(e)}")
            return False
    
    def process_folder_files(self, folder_path):
        files = [
            f for f in folder_path.iterdir()
            if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".pdf"]
        ]
        
        if not files:
            self.log("No supported files found in the folder.")
            return
        
        self.log(f"Found {len(files)} file(s) to process")
        success_count = 0
        
        for i, file_path in enumerate(files, 1):
            self.update_status(f"Processing {i}/{len(files)}: {file_path.name}")
            self.log(f"\n[{i}/{len(files)}] Processing: {file_path.name}")
            
            if self.process_single_file(file_path):
                success_count += 1
                self.log(f"✓ Success: {file_path.name}")
            
        self.log(f"\n{'='*60}")
        self.log(f"Completed: {success_count}/{len(files)} files processed successfully")


def main():
    root = tk.Tk()
    app = TextExtractorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
