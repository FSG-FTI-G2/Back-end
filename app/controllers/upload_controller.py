import os
from io import BytesIO
import asyncio
from fastapi import UploadFile
from app.models.user import UserSchema
from app.models.file import FileSchema, FileType, FileStatus
from app.providers import file_storage, state

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB


def __get_filetype(filename: str, capitalize: bool = True):
    if capitalize:
        return filename.split(".")[-1].upper()
    return filename.split(".")[-1].lower()


def __file_validator(filename: str, filebyte: bytes):
    # Validate file extension
    if __get_filetype(filename) not in FileType.__members__.keys():
        return False
    # Validate file size
    if len(filebyte) > MAX_FILE_SIZE:
        return False
    return True


def __update_status(user_id: str, filename: str, status: FileStatus, schema: FileSchema = None):
    # Update file state
    state.get(user_id)[filename] = status.value
    # Update file schema
    if schema is not None:
        schema.status = status
        schema.update()


async def __upload_file_controller(filename: str, filebyte: bytes, user: UserSchema):
    # Validate file
    if not __file_validator(filename, filebyte):
        __update_status(user.id, filename, FileStatus.ERROR)
        return
    print(f"Validated file: {filename}")
    # Create a file schema
    file_schema = FileSchema(
        user_id=user.id,
        type=FileType[__get_filetype(filename)],
        file_name=filename,
        file_path=filename,
        status=FileStatus.UPLOADING
    )
    file_schema.create()
    print(f"Uploading file: {filename}")
    try:
        # Read file content
        # Upload to MinIO
        file_storage.upload_file(filename, BytesIO(filebyte))
        # Update file status to processing
        __update_status(user.id, filename,
                        FileStatus.PROCESSING, file_schema)
        # TODO: Add extraction logic here
        # Update file status to success
        __update_status(user.id, filename,
                        FileStatus.SUCCESS, file_schema)
        return
    except Exception:
        # Update file status to error
        __update_status(user.id, filename, FileStatus.ERROR, file_schema)
        return


def upload_files_controller(files: list[tuple[str, bytes]], user: UserSchema):
    # Upload files in parallel
    for filename, filebyte in files:
        asyncio.run(__upload_file_controller(filename, filebyte, user))


def upload_file_status_controller(user_id: str) -> tuple[bool, dict[str, str]]:
    status = state.get(user_id)
    is_finished = all(
        [status.get(filename) in [FileStatus.SUCCESS.value, FileStatus.ERROR.value] for filename in status])
    return is_finished, status
