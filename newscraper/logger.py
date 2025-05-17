import logging
import os

if not os.path.exists("/app/logs"):
    os.makedirs("/app/logs")

logging.basicConfig(
    handlers=[
        logging.FileHandler("/app/logs/app.log"),  
        logging.StreamHandler() 
    ],
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)