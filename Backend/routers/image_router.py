from fastapi import APIRouter, UploadFile, File
from Backend.service.imager_tuner import tunning
from Backend.utils.tem_file_manager import save_temp_file, delete_temp_file
import os 
import cv2

router = APIRouter()

@router.post("/image_processing")
async def image_processing(file: UploadFile = File(...), type: str = "color", width: int = 100, height: int = 100):
    file_path = save_temp_file(file)
    try:
        processed_img = tunning(file_path, type, (width, height))
        _, img_encoded = cv2.imencode('.jpg', processed_img)
        return {"filename": file.filename, "content": img_encoded.tobytes()}
    finally:
        delete_temp_file(file_path)