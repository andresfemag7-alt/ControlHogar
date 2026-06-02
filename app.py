# app.py
import streamlit as st
from auth import authenticate_user, create_initial_users
from database import init_db

# 1. Configuración de la página
st.set_page_config(page_title="Control Hogar", page_icon="🏠", layout="wide")

# 2. Inicialización de Base de Datos y Usuarios
init_db()
create_initial_users()

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
                # Guardar el estado del usuario en la sesión
                st.session_state['logged_in'] = True
                st.session_state['username'] = user.username
                st.session_state['role'] = user.role
                st.success(f"¡Bienvenido {user.username}!")
                st.rerun() # Recarga la app para ocultar el login y mostrar el panel
            else:
                st.error("❌ Usuario o contraseña incorrectos.")

def main():
    # Inicializar el estado de sesión si no existe
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Mostrar login o el panel principal dependiendo del estado
    if not st.session_state['logged_in']:
        login_screen()
    else:
        # Menú lateral para usuarios autenticados
        st.sidebar.title(f"🏠 Panel de {st.session_state['username']}")
        st.sidebar.info(f"Rol: {st.session_state['role']}")
        
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state.clear()
            st.rerun()

        st.title("Panel de Control")
        st.write("¡El inicio de sesión funciona correctamente! Aquí integraremos las vistas específicas (Dashboard, Calendario, etc.) en el siguiente paso.")

if __name__ == "__main__":
    main()
