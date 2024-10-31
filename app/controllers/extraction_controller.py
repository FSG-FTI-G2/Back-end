from io import BytesIO
from docx import Document
from PyPDF2 import PdfReader
from app.models.user_schema import UserSchema
from app.models.file_schema import FileSchema, FileType
from app.providers import vector_db, embedder


async def extraction_features(text: str, file_schema: FileSchema, user: UserSchema):
    """
    Add features extracted from a file into Qdrant. This function takes the extracted
    text content and additional metadata from the file (via `FileSchema`) and stores
    them in the vector database (Qdrant) along with the payloads.

    Args:
    - text (str): The text content extracted from the file.
    - file_schema (FileSchema): The schema containing file information and metadata.
    """
    chunks = embedder.chunk_text(text)

    # Create a list of payloads to store metadata for each text chunk
    payloads = []
    for content in chunks:
        # Create the payload dictionary containing metadata to be stored in Qdrant
        payload = {
            "id": file_schema.id,
            "file_name": file_schema.file_name,
            "file_type": file_schema.type,
            "content": content
        }
        payloads.append(payload)

    # Embed the text chunks using the embedding
    embed_chunks = embedder.embed(chunks)

    # Add the extracted text and its metadata (payloads) to Qdrant
    vector_db.add_vectors(user.id, embed_chunks, payloads)


async def extraction_file_content(file_type: FileType, file_content: BytesIO):
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

    # Handling for unsupported file types
    else:
        raise ValueError(
            "Unsupported file type. Please provide a TXT, DOCX, or PDF file.")
