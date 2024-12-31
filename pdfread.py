import os
import time
from tkinter import Tk, filedialog, Label, Toplevel, Text, Scrollbar, Frame, END
from tkinter.ttk import Style, Progressbar, Button
from PyPDF2 import PdfReader
from transformers import pipeline
from threading import Thread
from datetime import datetime

def extract_pdf_text(pdf_path):
    """Extract text from a PDF file."""
    reader = PdfReader(pdf_path)
    all_text = ""
    for page in reader.pages:
        all_text += page.extract_text() + "\n"
    return all_text

def summarize_text(text):
    """Summarize the extracted text using a pre-trained model."""
    summarizer = pipeline("summarization", model="t5-small")
    max_chunk_size = 1000
    chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
    summaries = [summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunks]
    summary = " ".join(summaries)
    return "This document " + summary

def save_text_to_file(text, file_path):
    """Save text to a specified file."""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)

def show_confirmation_window(pdf_path):
    """Show a confirmation window with file details."""
    file_stats = os.stat(pdf_path)
    file_name = os.path.basename(pdf_path)
    file_size = round(file_stats.st_size / 1024, 2)
    word_count = len(extract_pdf_text(pdf_path).split())
    creation_date = datetime.fromtimestamp(file_stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S")

    confirm_window = Toplevel()
    confirm_window.title("Confirm PDF Details")
    confirm_window.geometry("400x300")

    Label(confirm_window, text=f"File Name: {file_name}").pack(pady=5)
    Label(confirm_window, text=f"File Size: {file_size} KB").pack(pady=5)
    Label(confirm_window, text=f"Word Count: {word_count}").pack(pady=5)
    Label(confirm_window, text=f"Date Created: {creation_date}").pack(pady=5)

    def run_summary():
        confirm_window.destroy()
        process_pdf(pdf_path)

    confirm_button = Button(confirm_window, text="Confirm", command=run_summary)
    confirm_button.pack(pady=20)

def process_pdf(pdf_path):
    """Process the PDF and update the UI with results."""
    result_folder = "result"
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    extracted_text = extract_pdf_text(pdf_path)
    extracted_text_path = os.path.join(result_folder, "PDFtext.txt")
    save_text_to_file(extracted_text, extracted_text_path)

    summary = summarize_text(extracted_text)
    summary_path = os.path.join(result_folder, "sum.txt")
    save_text_to_file(summary, summary_path)

    show_processing_window("Processing complete. Exiting...")
    time.sleep(2)
    os._exit(0)

def show_processing_window(message):
    """Show a loading or processing window."""
    loading_window = Toplevel()
    loading_window.title("Processing")
    loading_window.geometry("400x200")

    Label(loading_window, text=message, font=("Helvetica", 14)).pack(pady=20)
    progress_bar = Progressbar(loading_window, orient="horizontal", length=300, mode="indeterminate")
    progress_bar.pack(pady=20)
    progress_bar.start(10)
    
    loading_window.after(2000, loading_window.destroy)  # Automatically close after 2 seconds

def select_pdf():
    """Handle PDF selection and confirmation."""
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not pdf_path:
        print("No file selected. Exiting.")
        return
    show_confirmation_window(pdf_path)

def main():
    """Main function to create the UI."""
    root = Tk()
    root.title("PDF Text Extractor and Summarizer")
    root.geometry("400x250")

    style = Style()
    style.configure("TButton", font=("Helvetica", 12))

    Label(root, text="Welcome to PDF Text Extractor and Summarizer", font=("Helvetica", 16)).pack(pady=20)
    upload_button = Button(root, text="Select PDF", style="TButton", command=select_pdf)
    upload_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
