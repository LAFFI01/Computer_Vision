from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.routers.image_router import router as image_router

app = FastAPI(title="Image Processing API",version="1.0.0",description="API for basic image processing tasks using FastAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(image_router,
                    prefix="/image",
                    tags=["Image Processing"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Image Processing API"}