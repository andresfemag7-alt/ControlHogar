import streamlit as st
import datetime
import os
import bcrypt
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. CONFIGURACIÓN INICIAL Y ESTILOS
st.set_page_config(page_title="Control Hogar", page_icon="🏠", layout="wide")

# Estilos CSS Modernos
st.markdown("""
    <style>
    .tarjeta-tarea { background-color: #ffffff; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 15px; border-left: 6px solid #4CAF50; }
    .tarjeta-completada { background-color: #e8f5e9; border-radius: 12px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 15px; border-left: 6px solid #2e7d32; }
    .frase-motivacional { font-size: 18px; font-style: italic; color: #2c3e50; text-align: center; padding: 20px; background: #e3f2fd; border-radius: 12px; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# 2. BASE DE DATOS Y AUTENTICACIÓN (UNIFICADO)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String)

# Configuración de BD
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")
engine = create_engine(f'sqlite:///{db_path}', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def hash_pass(p): return bcrypt.hashpw(p.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
def verify_pass(p, h): return bcrypt.checkpw(p.encode('utf-8'), h.encode('utf-8'))

# Crear usuarios por defecto si no existen
db = SessionLocal()
if db.query(User).count() == 0:
    db.add_all([User(username="Roberti", password_hash=hash_pass("admin123"), role="Admin"),
                User(username="JuanManuel", password_hash=hash_pass("juan123"), role="Usuario")])
    db.commit()
db.close()

# 3. LÓGICA DE TIEMPO (COLOMBIA)
def obtener_datos_tiempo():
    tz_colombia = datetime.timezone(datetime.timedelta(hours=-5))
    ahora = datetime.datetime.now(tz_colombia)
    dias_es = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    return dias_es[ahora.weekday()], ahora.isocalendar()[1]

# 4. FUNCIONES DE INTERFAZ
def login_screen():
    st.title("🔐 Acceso a Control Hogar")
    u = st.text_input("Usuario")
    p = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        db = SessionLocal()
        user = db.query(User).filter(User.username == u).first()
        db.close()
        if user and verify_pass(p, user.password_hash):
            st.session_state.update({'logged_in': True, 'user': u})
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

def mostrar_panel_juan_manuel():
    dia, semana = obtener_datos_tiempo()
    st.title(f"📅 Panel de Juan Manuel - {dia}")
    st.markdown('<div class="frase-motivacional">🎓 <b>Objetivo UDENAR (Derecho):</b> El éxito exige preparación. ¡La constancia es la llave de tu futuro!</div>', unsafe_allow_html=True)
    
    # ICFES
    if dia in ["Lunes", "Martes", "Viernes"]:
        materia = "Lectura Crítica (Crucial para Derecho)" if dia == "Lunes" else "Ciencias Sociales y Ciudadanas" if dia == "Martes" else "Matemáticas y Razonamiento"
        st.subheader(f"📚 Estudio ICFES: {materia}")
        if st.checkbox("✅ Mesa limpia antes de empezar"):
            st.checkbox("✅ Completé mis 2 horas de estudio")
    
    # ASEO GENERAL (Cada 2 semanas - pares)
    if dia in ["Martes", "Jueves"]:
        if semana % 2 == 0:
            st.subheader("🧹 Aseo General (Semana de Aseo)")
            st.checkbox("Barrer, trapear y organizar áreas comunes")
        else:
            st.info("✨ Esta semana no te corresponde aseo general.")

    # UNIFORME
    if dia in ["Martes", "Miércoles", "Jueves"]:
        st.subheader("👔 Lavado de Uniforme (Obligatorio)")
        st.checkbox("Lavado y tendido de uniforme de diario")

    # DOMINGO PROFUNDO
    if dia == "Domingo":
        st.subheader("🧽 Aseo Profundo (Habitación)")
        st.checkbox("Limpieza debajo de cama, muebles y sacudido de polvo")

# 5. MENÚ PRINCIPAL
def main():
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
    
    if not st.session_state['logged_in']:
        login_screen()
    else:
        st.sidebar.title(f"🏠 {st.session_state['user']}")
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state.clear()
            st.rerun()
        
        menu = st.sidebar.radio("Navegación", ["Panel Diario", "Zona de Lavado"])
        
        if menu == "Panel Diario":
            mostrar_panel_juan_manuel()
        else:
            st.title("👕 Zona de Lavado")
            st.checkbox("Registrar uso de lavadora")

if __name__ == "__main__":
    main()
