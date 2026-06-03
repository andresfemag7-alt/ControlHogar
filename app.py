import streamlit as st
import datetime
import os
import bcrypt
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Configuración inicial
st.set_page_config(page_title="Control Hogar", page_icon="🏠", layout="wide")

# Base de datos embebida
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
engine = create_engine(f'sqlite:///{os.path.join(BASE_DIR, "database.db")}', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def hash_pass(p): return bcrypt.hashpw(p.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
def verify_pass(p, h): return bcrypt.checkpw(p.encode('utf-8'), h.encode('utf-8'))

# Crear usuarios si no existen
db = SessionLocal()
if db.query(User).count() == 0:
    db.add_all([User(username="Roberti", password_hash=hash_pass("admin123"), role="Admin"),
                User(username="JuanManuel", password_hash=hash_pass("juan123"), role="Usuario")])
    db.commit()
db.close()

# Función de Tiempo para Colombia
def obtener_datos_tiempo():
    tz_colombia = datetime.timezone(datetime.timedelta(hours=-5))
    ahora = datetime.datetime.now(tz_colombia)
    dias_es = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    return dias_es[ahora.weekday()], ahora.isocalendar()[1]

# Interfaz Principal
def main():
    # Inicialización segura
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
    
    if not st.session_state['logged_in']:
        st.title("🔐 Acceso a Control Hogar")
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.button("Entrar"):
            db = SessionLocal()
            user = db.query(User).filter(User.username == u).first()
            if user and verify_pass(p, user.password_hash):
                st.session_state.update({'logged_in': True, 'username': u})
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
    else:
        # Menú Lateral con acceso seguro al nombre de usuario
        nombre_usuario = st.session_state.get('username', 'Usuario')
        st.sidebar.title(f"🏠 {nombre_usuario}")
        
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state.clear()
            st.rerun()
        
        dia, semana = obtener_datos_tiempo()
        st.title(f"📅 Panel de Juan Manuel - {dia}")
        
        # Lógica de Tareas
        if dia in ["Lunes", "Martes", "Viernes"]:
            st.subheader(f"📚 Estudio ICFES: {'Lectura Crítica' if dia == 'Lunes' else 'Sociales' if dia == 'Martes' else 'Matemáticas'}")
            st.checkbox("✅ Mesa limpia")
            st.checkbox("✅ Completé 2 horas de estudio")
        
        if dia in ["Martes", "Jueves"] and semana % 2 == 0:
            st.subheader("🧹 Aseo General")
            st.checkbox("Barrer y trapear áreas comunes")

if __name__ == "__main__":
    main()
