# database.py
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Base para nuestros modelos de base de datos
Base = declarative_base()

# Definición de la tabla de usuarios
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String)

# --- NUEVO CÓDIGO ---
# Calculamos la ruta exacta de la carpeta donde está este archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Unimos esa ruta con el nombre de nuestro archivo de base de datos
db_path = os.path.join(BASE_DIR, "database.db")

# Le pasamos la ruta absoluta a SQLite (fíjate en las 3 barras /// y la variable)
engine = create_engine(f'sqlite:///{db_path}')
# --------------------

SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Crea las tablas en la base de datos si no existen."""
    Base.metadata.create_all(engine)
