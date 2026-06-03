import streamlit as st
import datetime
from datetime import timedelta
import os
import bcrypt
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Control Hogar", page_icon="🏠", layout="wide")

# ==========================================
# SECCIÓN 1: BASE DE DATOS Y AUTENTICACIÓN
# ==========================================
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")
engine = create_engine(f'sqlite:///{db_path}')
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_initial_users():
    db = SessionLocal()
    if db.query(User).count() == 0:
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
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if user and verify_password(password, user.password_hash):
        return user
    return None

init_db()
create_initial_users()

# ==========================================
# SECCIÓN 2: FUNCIONES DE INTERFAZ (UI)
# ==========================================

def aplicar_estilos():
    st.markdown("""
        <style>
        .tarjeta-tarea { background-color: #f8f9fa; border-radius: 10px; padding: 20px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px; border-top: 4px solid #4CAF50;}
        .tarjeta-completada { background-color: #e8f5e9; border-radius: 10px; padding: 20px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px; border-top: 4px solid #2e7d32;}
        .frase-motivacional { font-size: 18px; font-style: italic; color: #2c3e50; text-align: center; padding: 15px; background: #e3f2fd; border-radius: 10px; margin-bottom: 20px; }
        </style>
    """, unsafe_allow_html=True)

def login_screen():
    st.title("🔐 Acceso a Control Hogar")
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Entrar")
        if submit:
            user = authenticate_user(username, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = user.username
                st.session_state['role'] = user.role
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos.")

def obtener_dia_actual():
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    return dias[datetime.datetime.now().weekday()]

def es_semana_de_aseo_general():
    numero_semana = datetime.datetime.now().isocalendar()[1]
    return numero_semana % 2 == 0

def mostrar_panel_juan_manuel():
    dia_hoy = obtener_dia_actual()
    semana_activa = es_semana_de_aseo_general()
    st.title(f"📅 Panel de Juan Manuel - {dia_hoy}")
    # ... (El resto de la lógica de tareas que ya teníamos)
    st.info("Panel cargado correctamente.")

def main():
    aplicar_estilos()
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login_screen()
    else:
        # Aquí va la lógica de navegación que ya tenías
        st.sidebar.title(f"🏠 {st.session_state['username']}")
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state.clear()
            st.rerun()
        mostrar_panel_juan_manuel()

if __name__ == "__main__":
    main()
