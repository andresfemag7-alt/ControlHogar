import streamlit as st
import datetime
from datetime import timedelta
import os
import bcrypt
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser la primera instrucción)
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

# Inicializar Base de Datos
init_db()
create_initial_users()

# ==========================================
# SECCIÓN 2: INTERFAZ DE USUARIO (UI)
# ==========================================
def aplicar_estilos():
    st.markdown("""
        <style>
        .tarjeta-tarea { background-color: #f8f9fa; border-radius: 10px; padding: 20px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px; }
        .alerta-amarilla { background-color: #fff3cd; color: #856404; padding: 10px; border-radius: 5px; border-left: 5px solid #ffeeba; font-weight: bold; margin-top: 10px; }
        .sancion-roja { background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 8px; border-left: 5px solid #f5c6cb; font-weight: bold; font-size: 16px; }
        .frase-motivacional { font-size: 20px; font-style: italic; color: #2c3e50; text-align: center; padding: 20px; background: linear-gradient(to right, #e0eafc, #cfdef3); border-radius: 10px; margin-bottom: 20px; }
        </style>
    """, unsafe_allow_html=True)

def login_screen():
    st.title("🔐 Acceso a Control Hogar")
    st.markdown("Por favor, ingresa tus credenciales para acceder al sistema.")
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
                st.success(f"¡Bienvenido {user.username}!")
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos.")

def mostrar_panel_juan_manuel():
    st.title("Panel de Seguimiento: Juan Manuel")
    st.markdown('<div class="frase-motivacional">"El éxito no es un accidente. Es trabajo duro, perseverancia, aprendizaje, estudio, sacrificio y, sobre todo, amor por lo que estás haciendo." <br><br> 🎯 <b>Propósito:</b> Esta app te ayudará a construir hábitos sólidos, organizar tu tiempo para el ICFES y mantener la armonía en casa. ¡Tú puedes lograrlo!</div>', unsafe_allow_html=True)
    st.write("---")

    tab1, tab2, tab3 = st.tabs(["📅 Semana 1", "📅 Semana 2", "📊 Reporte y Sanciones"])

    with tab1:
        st.subheader("Horario y Tareas - Semana 1")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="tarjeta-tarea">', unsafe_allow_html=True)
            st.markdown("### 📚 Estudio ICFES")
            st.markdown("**Lunes, Martes y Viernes | 3:00 PM – 5:00 PM**")
            st.markdown("*Meta semanal: 6 horas mínimas*")
            mesa_limpia = st.checkbox("🧹 He limpiado la mesa de estudio antes de empezar (Obligatorio)")
            
            if mesa_limpia:
                st.info("Mesa lista. ¡A estudiar!")
                if st.session_state.get('role') == 'Usuario Evaluado':
                    st.button("Solicitar Validación de Estudio", disabled=False)
                    st.caption("Esperando que un Administrador apruebe esta tarea.")
                else:
                    if st.button("✅ Aprobar Estudio de Juan Manuel", type="primary", key="btn_aprobar_estudio"):
                        st.success("¡Estudio validado exitosamente!")
            else:
                st.warning("Debes limpiar la mesa para habilitar el estudio.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="tarjeta-tarea">', unsafe_allow_html=True)
            st.markdown("### 🛏️ Aseo de Habitación")
            st.markdown("**Martes y Jueves | 2:30 PM – 3:00 PM**")
            st.checkbox("Barrer y trapear", key="chk_barrer")
            st.checkbox("Organizar cama y escritorio", key="chk_cama")
            
            if st.session_state.get('role') != 'Usuario Evaluado':
                st.button("✅ Aprobar Aseo", key="btn_aprobar_aseo")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="tarjeta-tarea">', unsafe_allow_html=True)
        st.markdown("### 👕 Zona de Lavandería (Regla de 3 Horas)")
        st.markdown("**Uniformes (Martes y Miércoles) | 12:00 PM - 3:00 PM**")
        lavando = st.checkbox("Iniciar Lavado de Uniforme", key="chk_lavado")
        
        if lavando:
            hora_inicio_simulada = datetime.datetime.now() - timedelta(hours=4) 
            st.write("Lavadora en curso...")
            ropa_sacada = st.checkbox("Ropa sacada y tendida", key="chk_sacada")
            tiempo_transcurrido = datetime.datetime.now() - hora_inicio_simulada
            
            if not ropa_sacada and tiempo_transcurrido.total_seconds() > 10800:
                st.markdown('<div class="alerta-amarilla">⚠️ ALERTA: Han pasado más de 3 horas desde que inició la lavadora. Por favor, saca la ropa inmediatamente.</div>', unsafe_allow_html=True)
            elif ropa_sacada:
                st.success("¡Ropa gestionada a tiempo!")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.subheader("Horario y Tareas - Semana 2")
        st.info("Las tareas de la Semana 1 se repiten, con una adición importante de fin de ciclo.")
        st.markdown('<div class="tarjeta-tarea">', unsafe_allow_html=True)
        st.markdown("### 🧼 Tarea Obligatoria de Fin de Quincena")
        st.markdown("Aplica para: **Todos los usuarios de la casa**")
        st.checkbox("Realizar aseo profundo de la zona asignada", key="chk_profundo")
        st.checkbox("Doblar toda la ropa limpia", key="chk_doblar")
        
        if st.session_state.get('role') != 'Usuario Evaluado':
             st.button("✅ Confirmar Aseo Profundo", key="btn_aprobar_profundo")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.subheader("Panel de Sanciones y Reportes")
        sancion_activa = True 
        
        if sancion_activa:
            st.markdown('<div class="sancion-roja">🚨 ESTADO: REPORTADO<br><br>Has incumplido una de las tareas críticas.<br><b>PENITENCIA ACTIVA:</b> Debes traer mecato para todos en la casa para poder quitarte esta sanción. <br><br>❌ Restricciones: Sin salidas, sin internet libre, sin teléfono tarde.</div>', unsafe_allow_html=True)
            if st.session_state.get('role') != 'Usuario Evaluado':
                st.write("---")
                st.write("**Opciones de Administrador:**")
                if st.button("Levantar Sanción (Entregó el mecato)", key="btn_levantar"):
                    st.success("Sanción levantada exitosamente.")
        else:
            st.success("¡Excelente comportamiento! No hay sanciones activas.")
            st.balloons()

def mostrar_panel_otros():
    st.title("Panel General")
    st.info("Aquí se construirán las tareas específicas para Roberti, Karol y Felipe en el futuro.")

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
        st.sidebar.subheader("Navegación")
        
        opciones_menu = ["Panel de Juan Manuel", "Panel General"]
        seleccion = st.sidebar.radio("Ir a:", opciones_menu)
        
        st.sidebar.markdown("---")
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state.clear()
            st.rerun()

        if seleccion == "Panel de Juan Manuel":
            mostrar_panel_juan_manuel()
        elif seleccion == "Panel General":
            mostrar_panel_otros()

if __name__ == "__main__":
    main()
