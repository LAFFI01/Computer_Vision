import numpy as np 
import cv2 
import os
from Backend.core.config import setting

def tunning(path:str,type:str,size:tuple):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Image not found at path: {path}")

    if type == "grayscale":
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    elif type == "binary":
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    
    elif type == "color":
        # No color conversion needed, just resizing
        pass
    
    processed_img = cv2.resize(img, size)
    return processed_img