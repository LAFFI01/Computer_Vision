import os 
from dotenv import load_dotenv 

load_dotenv()

class setting:
    TEMP_PATH = os.getenv("TEMP_PATH", "/tmp/fs.jpg")
setting = setting()