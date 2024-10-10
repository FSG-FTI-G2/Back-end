import os
from fastapi.responses import JSONResponse, HTMLResponse
from app.controllers.static_file_serving import retrieve_file
from fastapi import APIRouter

router = APIRouter()

# Route to download file
@router.get("/download/{input_file}")
def download_file(input_file: str):
    file_path = os.path.join("temp", input_file)
    print(f"Attempting to download file from path: {file_path}")  # Debug statement
    file = retrieve_file(input_file, file_path)
    if file:
        return JSONResponse(content={"message": f"File {input_file} downloaded."})
    else:
        return JSONResponse(content={"message": f"File {input_file} already exists."})
    