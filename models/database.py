from sqlalchemy import create_engine
from decouple import config

class Database:
    def __init__(self):
        # Cargar las variables de entorno desde el archivo .env
        POSTGRES_USER = config('POSTGRES_USER')
        POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
        POSTGRES_HOST = config('POSTGRES_HOST')
        POSTGRES_DATABASE = config('POSTGRES_DATABASE')
        POSTGRES_PORT = config('POSTGRES_PORT')

        # Crear la cadena de conexión para SQLAlchemy
        self.DB_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

        # Crear el motor de SQLAlchemy
        self.engine = create_engine(self.DB_URL)
