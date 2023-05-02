import sys
import nltk
nltk.download('punkt')
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit


class App(QWidget):

    def __init__(self):
        super().__init__()

        # Create the upload button
        self.upload_button = QPushButton("Upload PDF", self)
        self.upload_button.clicked.connect(self.upload_pdf)
        self.upload_button.setGeometry(20, 20, 120, 30)

        # Create the URL input field
        self.url_input = QLineEdit(self)
        self.url_input.setGeometry(150, 20, 300, 30)

        # Create the analyze button
        self.analyze_button = QPushButton("Analyze", self)
        self.analyze_button.clicked.connect(self.analyze_pdf)
        self.analyze_button.setGeometry(460, 20, 120, 30)

        # Create the output label
        self.output_label = QTextEdit(self)
        self.output_label.setGeometry(20, 70, 560, 300)

        # Create the error label
        self.error_label = QLabel(self)
        self.error_label.setGeometry(20, 380, 560, 20)

        # Create the text box
        self.text_box = QTextEdit(self)
        self.text_box.setGeometry(20, 420, 560, 200)
        self.text_box.setReadOnly(True)

        # Create the text label for the name of the PDF file
        self.pdf_name_label = QLabel(self)
        self.pdf_name_label.setGeometry(20, 200, 560, 20)

    def upload_pdf(self):
        # Get the file name
        filename, _ = QFileDialog.getOpenFileName(self, "Upload PDF", "", "PDF files (*.pdf)")

        # Check if the file is a PDF
        if not filename.endswith(".pdf"):
            self.error_label.setText("Please select a PDF file")
            return

        # Read the PDF file
        with open(filename, "rb") as f:
            try:
                pdf_text = f.read().decode("utf-8")
            except UnicodeDecodeError:
                self.error_label.setText("The file is not in UTF-8 encoding.")
                return

        # Set the URL input field to the selected file path
        self.url_input.setText(filename)

        # Display the content of the PDF file in the text box
        self.text_box.setText(pdf_text)

        # Output the name of the PDF file
        self.pdf_name_label.setText("PDF File Name: {}".format(filename))

        # Print out "PDF is uploaded successfully"
        self.output_label.insertHtml("<p style='color:red;'>PDF is uploaded successfully</p>")

        # Convert PDF to TXT file
        with open(filename[:-4] + ".txt", "w") as f:
            f.write(self.text_box.toPlainText())

    def analyze_pdf(self):
        # Create a list of sentences
        sentences = nltk.sent_tokenize(self.text_box.toPlainText())

        # Create a list of named entities
        named_entities = nltk.ne_chunk(sentences)

        # Summarize the PDF file
        summarizer = transformers.pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")
        summary = summarizer(self.text_box.toPlainText(), max_length=100)

        # Print the summarized version of the PDF file into the QTextEdit
        self.output_label.setText(summary)

    def run(self):
        self.setGeometry(100, 100, 600, 420)
        self.setWindowTitle("PDF Analyzer")
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex.run()
    sys.exit(app.exec_())

