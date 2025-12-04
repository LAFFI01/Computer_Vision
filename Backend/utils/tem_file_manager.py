import os 
import shutil
from Backend.core.config import setting
from fastapi import UploadFile, File, HTTPException

def save_temp_file(file: UploadFile ):
    folder = setting.TEMP_PATH
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, file.filename)
    try:
        with open(file_path, "wb") as f:
            f.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    return file_path

def delete_temp_file(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")