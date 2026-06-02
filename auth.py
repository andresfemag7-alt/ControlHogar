# auth.py
import bcrypt
from database import SessionLocal, User

def hash_password(password):
    """Convierte una contraseña de texto plano en un hash seguro."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """Verifica si la contraseña ingresada coincide con el hash guardado."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_initial_users():
    """Crea los usuarios predeterminados si la base de datos está vacía."""
    db = SessionLocal()
    if db.query(User).count() == 0:
        # Aquí asignamos una contraseña temporal 'admin123' a los administradores y 'juan123' a Manuel.
        # Bcrypt se encargará de encriptarlas antes de guardarlas.
        users = [
            User(username="Roberti", password_hash=hash_password("admin123"), role="Administrador Principal"),
            User(username="Karol", password_hash=hash_password("admin123"), role="Viceadministradora"),
            User(username="Felipe", password_hash=hash_password("admin123"), role="Administrador General"),
            User(username="JuanManuel", password_hash=hash_password("juan123"), role="Usuario Evaluado")
        ]
        db.add_all(users)
        db.commit()
    db.close()

def authenticate_user(username, password):
    """Busca al usuario y verifica su contraseña."""
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    
    if user and verify_password(password, user.password_hash):
        return user
    return None
