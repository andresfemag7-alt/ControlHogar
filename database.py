# database.py
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

# Crear el motor de la base de datos SQLite (se creará un archivo database.db)
engine = create_engine('sqlite:///database.db')
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Crea las tablas en la base de datos si no existen."""
    Base.metadata.create_all(engine)
