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
# SECCIÓN 2: INTERFAZ Y LÓGICA DE DÍAS
# ==========================================
def aplicar_estilos():
    st.markdown("""
        <style>
        .tarjeta-tarea { background-color: #f8f9fa; border-radius: 10px; padding: 20px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px; border-top: 4px solid #4CAF50;}
        .tarjeta-completada { background-color: #e8f5e9; border-radius: 10px; padding: 20px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px; border-top: 4px solid #2e7d32;}
        .alerta-amarilla { background-color: #fff3cd; color: #856404; padding: 10px; border-radius: 5px; border-left: 5px solid #ffeeba; font-weight: bold; margin-top: 10px; }
        .frase-motivacional { font-size: 18px; font-style: italic; color: #2c3e50; text-align: center; padding: 15px; background: #e3f2fd; border-radius: 10px; margin-bottom: 20px; }
        </style>
    """, unsafe_allow_html=True)

def obtener_dia_actual():
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    return dias[datetime.datetime.now().weekday()]

def es_semana_de_aseo_general():
    """Calcula si la semana actual es par para alternar el aseo cada dos semanas."""
    numero_semana = datetime.datetime.now().isocalendar()[1]
    return numero_semana % 2 == 0

def mostrar_panel_juan_manuel():
    dia_hoy = obtener_dia_actual()
    semana_activa = es_semana_de_aseo_general()
    
    st.title(f"📅 Panel de Juan Manuel - Hoy es {dia_hoy}")
    st.markdown('<div class="frase-motivacional">🎓 <b>Objetivo UDENAR (Derecho):</b> El éxito exige preparación. Un puntaje alto en Lectura Crítica y Sociales será tu mejor aliado. ¡Esfuérzate hoy para celebrar mañana!</div>', unsafe_allow_html=True)
    
    st.subheader(f"Tus tareas asignadas para hoy ({dia_hoy})")
    
    # 1. ESTUDIO ICFES
    if dia_hoy in ["Lunes", "Martes", "Viernes"]:
        recomendacion = "Lectura Crítica 📖" if dia_hoy == "Lunes" else "Ciencias Sociales y Ciudadanas 🌍" if dia_hoy == "Martes" else "Matemáticas y Ciencias 📐"
        
        mesa_limpia = st.checkbox("🧹 He limpiado la mesa de estudio antes de empezar", key="mesa_icfes")
        estudio_hecho = st.checkbox("📚 Completé mis 2 horas de estudio", key="estudio_icfes", disabled=not mesa_limpia)
        
        if estudio_hecho:
            st.markdown('<div class="tarjeta-completada">✅ <b>Tareas de sección (Estudio) ya realizadas.</b> ¡Excelente trabajo!</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="tarjeta-tarea"><h3>📚 Estudio ICFES (3:00 PM - 5:00 PM)</h3><p><b>Recomendación para Derecho (UDENAR):</b> Enfócate hoy en <b>{recomendacion}</b>.</p></div>', unsafe_allow_html=True)

    # 2. ASEO GENERAL DE LA CASA (CADA DOS SEMANAS)
    if dia_hoy in ["Martes", "Jueves"]:
        if semana_activa:
            aseo_hecho = st.checkbox("🧹 Completé el aseo general de la casa", key="aseo_general")
            if aseo_hecho:
                st.markdown('<div class="tarjeta-completada">✅ <b>Tareas de sección (Aseo General) ya realizadas.</b></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="tarjeta-tarea"><h3>🧹 Aseo General de la Casa (2:30 PM - 3:00 PM)</h3><p>Esta semana <b>SÍ</b> te corresponde el aseo general de las áreas comunes.</p></div>', unsafe_allow_html=True)
        else:
            st.info("✨ **Aseo General:** Esta semana NO te corresponde el aseo general de la casa (recuerda que es cada dos semanas). ¡Aprovecha el tiempo para estudiar!")

    # 3. UNIFORME OBLIGATORIO DE DIARIO
    if dia_hoy in ["Martes", "Miércoles", "Jueves"]:
        uniforme_lavado = st.checkbox("👕 Uniforme de diario lavado y colgado", key="uniforme_diario")
        
        if uniforme_lavado:
             st.markdown('<div class="tarjeta-completada">✅ <b>Tareas de sección (Uniforme) ya realizadas.</b></div>', unsafe_allow_html=True)
        else:
             st.markdown('<div class="tarjeta-tarea"><h3>👔 Lavado de Uniforme (Obligatorio)</h3><p>Debes lavar tu uniforme de diario apenas llegues. ¡No lo dejes acumular!</p></div>', unsafe_allow_html=True)

    # 4. ASEO PROFUNDO DOMINICAL
    if dia_hoy == "Domingo":
        aseo_profundo = st.checkbox("🧽 Realicé aseo profundo de mi habitación (debajo de cama y muebles)", key="aseo_prof")
        if aseo_profundo:
             st.markdown('<div class="tarjeta-completada">✅ <b>Aseo profundo dominical finalizado.</b> Ambiente libre de polvo.</div>', unsafe_allow_html=True)
        else:
             st.markdown('<div class="tarjeta-tarea"><h3>🧽 Aseo Profundo (Prevención de Enfermedades)</h3><p>Hoy toca limpieza a fondo: barrer y trapear debajo de la cama y sacudir muebles para evitar acumulación de polvo y alergias.</p></div>', unsafe_allow_html=True)

    # Mensaje si no hay tareas
    if dia_hoy not in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Domingo"]:
        st.info("Hoy es un día libre de tareas programadas obligatorias. ¡Aprovecha para descansar o adelantar trabajo!")

def mostrar_zona_lavanderia():
    """Zona general para el uso de la lavadora por cualquier miembro de la casa."""
    st.title("👕 Zona General de Lavandería")
    st.write("Cualquier miembro de la casa puede registrar el uso de la lavadora aquí.")
    
    st.markdown('<div class="tarjeta-tarea">', unsafe_allow_html=True)
    lavando = st.checkbox("Iniciar uso general de la lavadora", key="chk_lavado_general")
    if lavando:
        st.write("Lavadora en curso...")
        ropa_sacada = st.checkbox("Ropa sacada y tendida", key="chk_sacada_general")
        if not ropa_sacada:
            st.info("Recuerda que tienes un máximo de 3 horas para sacar la ropa. Si superas este tiempo, se generará una alerta a los administradores.")
        else:
            st.success("✅ ¡Lavandería general gestionada con éxito!")
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    aplicar_estilos()
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login_screen()
    else:
        st.sidebar.title(f"🏠 {st.session_state['username']}")
        st.sidebar.info(f"Rol: {st.session_state['role']}")
        st.sidebar.markdown("---")
        
        opciones_menu = ["Panel de Juan Manuel", "Zona de Lavandería", "Panel General (Otros)"]
        seleccion = st.sidebar.radio("Ir a:", opciones_menu)
        
        st.sidebar.markdown("---")
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state.clear()
            st.rerun()

        if seleccion == "Panel de Juan Manuel":
            mostrar_panel_juan_manuel()
        elif seleccion == "Zona de Lavandería":
            mostrar_zona_lavanderia()
        elif seleccion == "Panel General (Otros)":
            st.title("Panel General")
            st.info("Aquí se construirán las tareas de los demás miembros de la casa.")

if __name__ == "__main__":
    main()
