import logging


logging.basicConfig(
    handlers=[
        logging.StreamHandler() 
    ],
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)