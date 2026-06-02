import streamlit as st
import datetime
from datetime import timedelta
from auth import authenticate_user, create_initial_users
from database import init_db

# 1. Configuración de la página (DEBE SER LA PRIMERA INSTRUCCIÓN DE STREAMLIT)
st.set_page_config(page_title="Control Hogar", page_icon="🏠", layout="wide")

# 2. Inicialización de Base de Datos y Usuarios
init_db()
create_initial_users()

def aplicar_estilos():
    """Aplica el diseño visual moderno a la aplicación."""
    st.markdown("""
        <style>
        .tarjeta-tarea {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        }
        .alerta-amarilla {
            background-color: #fff3cd;
            color: #856404;
            padding: 10px;
            border-radius: 5px;
            border-left: 5px solid #ffeeba;
            font-weight: bold;
            margin-top: 10px;
        }
        .sancion-roja {
            background-color: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            border-left: 5px solid #f5c6cb;
            font-weight: bold;
            font-size: 16px;
        }
        .frase-motivacional {
            font-size: 20px;
            font-style: italic;
            color: #2c3e50;
            text-align: center;
            padding: 20px;
            background: linear-gradient(to right, #e0eafc, #cfdef3);
            border-radius: 10px;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

def login_screen():
    """Muestra el formulario de inicio de sesión."""
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
    """Genera la interfaz visual del dashboard de Juan Manuel con validaciones y estilos."""
    
    st.title("Panel de Seguimiento: Juan Manuel")
    
    # SECCIÓN DE MOTIVACIÓN
    st.markdown('<div class="frase-motivacional">"El éxito no es un accidente. Es trabajo duro, perseverancia, aprendizaje, estudio, sacrificio y, sobre todo, amor por lo que estás haciendo." <br><br> 🎯 <b>Propósito:</b> Esta app te ayudará a construir hábitos sólidos, organizar tu tiempo para el ICFES y mantener la armonía en casa. ¡Tú puedes lograrlo!</div>', unsafe_allow_html=True)
    st.write("---")

    # SISTEMA DE TABS
    tab1, tab2, tab3 = st.tabs(["📅 Semana 1", "📅 Semana 2", "📊 Reporte y Sanciones"])

    with tab1:
        st.subheader("Horario y Tareas - Semana 1")
        col1, col2 = st.columns(2)
        
        # TARJETA ICFES
        with col1:
            st.markdown('<div class="tarjeta-tarea">', unsafe_allow_html
