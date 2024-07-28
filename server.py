import logging
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting the server...")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="info")
