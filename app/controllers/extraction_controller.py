from app.models.file import FileSchema, FileType
from app.providers import qdrant_client
from io import BytesIO
from docx import Document 
from PyPDF2 import PdfReader 
from app.utils.text_processing_utils import chunk_text


def extraction_features(text: str, file_schema: FileSchema):
    """
    Add features extracted from a file into Qdrant. This function takes the extracted
    text content and additional metadata from the file (via `FileSchema`) and stores
    them in the vector database (Qdrant) along with the payloads.
    
    Args:
    - text (str): The text content extracted from the file.
    - file_schema (FileSchema): The schema containing file information and metadata.
    """
    chunks = chunk_text(text)
    
    for content in chunks:
        # Create the payload dictionary containing metadata to be stored in Qdrant
        payloads = {
            "id": file_schema.id,  # File ID
            "user_id": file_schema.user_id,  # ID of the user who uploaded the file
            "file_name": file_schema.file_name,  # Name of the file
            "file_type": file_schema.type,  # Type of the file (e.g., PDF, DOCX, TXT)
            "file_path": file_schema.file_path,  # Path where the file is stored
            "content": content
        }
    
        # Add the extracted text and its metadata (payloads) to Qdrant
        qdrant_client.add_vectors(text, payloads)


def extraction_file_content(file_type: FileType, file_content: BytesIO):
    """
    Reads and extracts text content from a file stream based on the file type (TXT, DOCX, or PDF).
    
    Args:
    - file_type (FileType): The type of file (TXT, DOCX, PDF).
    - file_content (BytesIO): The byte stream of the file content to be read.

    Returns:
    - str: The extracted text content from the file.
    """

    # Handling for plain text files
    if file_type == FileType.TXT:
        # Ensure the file stream is at the beginning
        file_content.seek(0)
        # Read the content of the text file and decode it from bytes to string
        content = file_content.read().decode('utf-8')
        return content

    # Handling for DOCX files (Word documents)
    elif file_type == FileType.DOCX:
        # Ensure the file stream is at the beginning
        file_content.seek(0)
        # Read the DOCX content using python-docx
        document = Document(file_content)
        # Extract all paragraphs and join them into a single text block
        content = "\n".join([para.text for para in document.paragraphs])
        return content

    # Handling for PDF files
    elif file_type == FileType.PDF:
        # Ensure the file stream is at the beginning
        file_content.seek(0)
        # Initialize the PDF reader to read the file
        reader = PdfReader(file_content)
        content = ""
        # Extract text from all pages and append them together
        for page in reader.pages:
            content += page.extract_text() + "\n"
        return content
