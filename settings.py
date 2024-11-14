import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_FOLDER = os.getenv('DB_FOLDER', './vector_store')
    PUBLIC_TEXT_FILES_FOLDER = os.getenv('PUBLIC_TEXT_FILES_FOLDER', './public_files')
    PRIVATE_TEXT_FILES_FOLDER = os.getenv('PRIVATE_TEXT_FILES_FOLDER', './team_files')
    INDIVIDUAL_TEXT_FILES_FOLDER = os.getenv('INDIVIDUAL_TEXT_FILES_FOLDER', './personal_files')
    GROQ_KEY = os.getenv('GROQ_KEY')
    QDRANT_URL = os.getenv('QDRANT_URL')
    QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
    GROQ_MODEL = os.getenv('GROQ_MODEL')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 500))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 100))

    @classmethod
    def check(cls):
        required =   'GROQ_KEY', 'GROQ_MODEL', #['OPENAI_API_KEY']
        for var in required:
            if not getattr(cls, var):
                raise ValueError(f"Missing {var} in environment")
