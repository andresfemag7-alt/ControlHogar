import streamlit as st
import datetime
from datetime import timedelta
import os
import bcrypt
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Configuración inicial
st.set_page_config(page_title="Control Hogar", page_icon="🏠", layout="wide")

# Base de datos y Auth embebidos
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
engine = create_engine(f'sqlite:///{os.path.join(BASE_DIR, "database.db")}')
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

# UI y Lógica
def main():
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
    
    if not st.session_state['logged_in']:
        st.title("🔐 Login")
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.button("Entrar"):
            db = SessionLocal()
            user = db.query(User).filter(User.username == u).first()
            if user and verify_pass(p, user.password_hash):
                st.session_state.update({'logged_in': True, 'user': u})
                st.rerun()
    else:
        st.sidebar.button("Cerrar Sesión", on_click=lambda: st.session_state.clear())
        
        dia = datetime.datetime.now().strftime("%A")
        semana = datetime.datetime.now().isocalendar()[1]
        
        st.title(f"📅 Panel de Juan Manuel - {dia}")
        st.info("🎓 Objetivo UDENAR: ¡Lectura Crítica y Sociales son la clave para Derecho!")

        # Tareas ICFES
        if dia in ["Monday", "Tuesday", "Friday"]:
            materia = "Lectura Crítica" if dia == "Monday" else "Sociales" if dia == "Tuesday" else "Matemáticas"
            st.subheader(f"📚 Estudio ICFES: {materia}")
            if st.checkbox("Mesa limpia"):
                st.checkbox("Completé 2 horas de estudio")
        
        # Aseo General (Cada 2 semanas - semanas pares)
        if dia in ["Tuesday", "Thursday"]:
            if semana % 2 == 0:
                st.subheader("🧹 Aseo General de la casa")
                st.checkbox("Barrer y trapear áreas comunes")
            else:
                st.write("✨ Esta semana no te corresponde aseo general.")

        # Uniforme
        if dia in ["Tuesday", "Wednesday", "Thursday"]:
            st.subheader("👔 Lavado de Uniforme (Obligatorio)")
            st.checkbox("Lavado y tendido")

        if dia == "Sunday":
            st.subheader("🧽 Aseo Profundo de habitación")
            st.checkbox("Limpieza debajo de cama y muebles")

if __name__ == "__main__": main()
