import unittest
from io import BytesIO
from docx import Document
from PyPDF2 import PdfWriter
from app.models.file import FileType
from app.controllers.extraction_controller import extraction_file_content


class TestExtractFileContent(unittest.TestCase):

    def setUp(self):
        # TXT file
        self.txt_file_name = "example.txt"
        self.txt_file_type = FileType.TXT
        self.txt_file_stream = BytesIO(b"This is an example of a text file content.")
        
        # DOCX file by creating local for test
        self.docx_file_name = "example.docx"
        self.docx_file_type = FileType.DOCX
        self.docx_file_stream = self.create_docx_file_stream()

        # PDF file by creating local for test
        self.pdf_file_type = FileType.PDF
        self.pdf_file_stream = self.create_sample_pdf_file_stream()

    def create_docx_file_stream(self):
        """Create a DOCX file and return its byte stream."""
        doc_stream = BytesIO()
        doc = Document()
        doc.add_paragraph("This is a test DOCX file content.")
        doc.save(doc_stream)
        doc_stream.seek(0)
        return doc_stream

    def create_sample_pdf_file_stream(self):
        """Create a PDF file with sample text content and return its byte stream."""
        pdf_stream = BytesIO()
        writer = PdfWriter()

        # Create a new page in the PDF with sample text
        writer.add_blank_page(width=200, height=300)

        # Add text content to the PDF
        writer.add_page(writer.pages[0])
        pdf_text = (
            "Sample PDF Document\n\n"
            "This is a test PDF file created for testing purposes.\n"
            "It contains multiple lines of text to verify the reading function.\n\n"
            "1. Introduction\n"
            "2. Sample Data\n"
            "3. Conclusion\n"
        )

        # Adding a new page with the text
        writer.get_page(0).insert_text(pdf_text)

        # Write to BytesIO stream
        writer.write(pdf_stream)
        pdf_stream.seek(0)  # Reset the stream position to the beginning
        return pdf_stream

    def test_txt_file_content(self):
        """Test for TXT file content extraction."""
        content = extraction_file_content(self.txt_file_type, self.txt_file_stream)
        expected_content = "This is an example of a text file content."
        self.assertEqual(content, expected_content, "TXT file content did not match.")

    def test_docx_file_content(self):
        """Test for DOCX file content extraction."""
        content = extraction_file_content(self.docx_file_type, self.docx_file_stream)
        expected_content = "This is a test DOCX file content."
        self.assertEqual(content, expected_content, "DOCX file content did not match.")

    def test_pdf_file_content(self):
        """Test for PDF file content extraction from the generated PDF file."""
        content = extraction_file_content(self.pdf_file_type, self.pdf_file_stream)
        print(content)  # Print the extracted text from the PDF file for verification

        # Set up assertions to check expected content
        expected_content = "Sample PDF Document"
        self.assertIn(expected_content, content, "Expected content not found in PDF.")

        expected_lines = [
            "This is a test PDF file created for testing purposes.",
            "It contains multiple lines of text to verify the reading function.",
            "1. Introduction",
            "2. Sample Data",
            "3. Conclusion",
        ]
        for line in expected_lines:
            self.assertIn(line, content, f"Expected line '{line}' not found in PDF content.")