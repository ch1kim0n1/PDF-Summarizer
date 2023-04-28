import nltk
import nltk
nltk.download('punkt')
import tkinter as tk

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        # Create the main window
        self.main_window = tk.Frame(self)
        self.main_window.pack(side="top", fill="both", expand=True)

        # Create the upload button
        self.upload_button = tk.Button(self.main_window, text="Upload PDF", command=self.upload_pdf)
        self.upload_button.pack(side="left")

        # Create the URL input field
        self.url_input = tk.Entry(self.main_window)
        self.url_input.pack(side="left")

        # Create the analyze button
        self.analyze_button = tk.Button(self.main_window, text="Analyze", command=self.analyze_pdf)
        self.analyze_button.pack(side="left")

        # Create the output label
        self.output_label = tk.Label(self.main_window, text="")
        self.output_label.pack(side="left")

        # Create the error label
        self.error_label = tk.Label(self.main_window, text="")
        self.error_label.pack(side="left")

        # Bind the event handlers
        self.upload_button.bind("<Button-1>", self.upload_pdf)
        self.analyze_button.bind("<Button-1>", self.analyze_pdf)

    def upload_pdf(self, event):
        # Get the file name
        filename = tk.filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

        # Check if the file is a PDF
        if not filename.endswith(".pdf"):
            self.error_label.config(text="Please select a PDF file")
            return

        # Read the PDF file
        with open(filename, "rb") as f:
            pdf_text = f.read()

        # Analyze the PDF file
        self.analyze_pdf(pdf_text)

    def analyze_pdf(self, pdf_text):
        # Create a list of sentences
        sentences = nltk.sent_tokenize(pdf_text)

        # Create a list of named entities
        named_entities = nltk.ne_chunk(sentences)

        # Print the named entities
        for entity in named_entities:
            self.output_label.config(text=self.output_label.cget("text") + entity + "\n")

    def main(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.main()
