from waitress import serve
from app import app  # Import the FastAPI app

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)
