import streamlit as st
import psycopg2
import pandas as pd
import datetime
import bcrypt
from utils.css import load_css

# --- LÓGICA DE CONEXIÓN ROBUSTA ---
@st.cache_resource
def init_connection():
    return psycopg2.connect(st.secrets["DB_CONNECTION_STRING"])

def get_connection():
    conn = init_connection()
    try:
        conn.cursor().execute("SELECT 1")
    except (psycopg2.InterfaceError, psycopg2.OperationalError, psycopg2.errors.InFailedSqlTransaction):
        # Si hay un error, hacer rollback y limpiar la caché
        if not conn.closed:
            conn.rollback()
        st.cache_resource.clear()
        conn = init_connection()
    return conn

# --- FUNCIÓN DE VERIFICACIÓN (Devuelve el nombre completo) ---
def check_login(username, password):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT password_hash, nombre_completo FROM usuarios WHERE username = %s", (username,))
            result = cur.fetchone()
            
            if result:
                stored_hash = result[0].encode('utf-8')
                nombre_completo = result[1]
                password_bytes = password.encode('utf-8')
                
                if bcrypt.checkpw(password_bytes, stored_hash):
                    return nombre_completo 
            return None
    except (psycopg2.InterfaceError, psycopg2.OperationalError, psycopg2.errors.InFailedSqlTransaction) as e:
        # Error de conexión o transacción fallida
        if not conn.closed:
            conn.rollback()
        st.cache_resource.clear()
        st.error("Error de conexión a la base de datos. Por favor, intenta de nuevo.")
        return None
    except Exception as e:
        st.error(f"Error al verificar: {e}")
        return None

# --- LÓGICA PRINCIPAL DE LA APP (EL "PORTERO") ---

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- SISTEMA DE TIMEOUT DE SESIÓN ---
if "last_activity" not in st.session_state:
    st.session_state.last_activity = datetime.datetime.now()

if "session_timeout_minutes" not in st.session_state:
    st.session_state.session_timeout_minutes = 60  # 60 minutos de inactividad

# Verificar timeout de sesión si está logueado
if st.session_state.logged_in:
    now = datetime.datetime.now()
    time_since_activity = (now - st.session_state.last_activity).total_seconds() / 60  # en minutos
    
    if time_since_activity > st.session_state.session_timeout_minutes:
        # Session expired
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.nombre_completo = None
        st.session_state.show_timeout_message = True
    else:
        # Actualizar última actividad
        st.session_state.last_activity = now

# --- 2. SI NO HA HECHO LOGIN (Mostrar solo el formulario) ---
if not st.session_state.logged_in:
    
    st.set_page_config(page_title="Inicio de Sesión", layout="centered")
    load_css()
    
    # --- CAMBIO CLAVE (Soluciona Problema 2) ---
    # Inyecta CSS para OCULTAR la barra lateral por completo
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("Sistema de Gestión 🔑")
    
    # Mostrar mensaje de timeout si existe
    if hasattr(st.session_state, 'show_timeout_message') and st.session_state.show_timeout_message:
        st.error("🕒 Tu sesión ha expirado por inactividad. Por favor, inicia sesión nuevamente.")
        # Limpiar el mensaje después de mostrarlo
        del st.session_state.show_timeout_message
    
    st.subheader("Por favor, inicia sesión para continuar")

    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Ingresar")
        
        if submitted:
            nombre_usuario = check_login(username, password) 
            
            if nombre_usuario:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.nombre_completo = nombre_usuario
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

# --- 3. SI SÍ HIZO LOGIN (Mostrar la app completa) ---
else:
    # Configuración de la página principal (la barra se muestra por defecto)
    st.set_page_config(
        page_title="Dashboard Principal",
        layout="wide"
    )
    load_css()

    # --- CAMBIO CLAVE (Soluciona Problema 1) ---
    # Construimos nuestro propio menú "bonito"
    with st.sidebar:
        st.title(f"Bienvenido, {st.session_state.nombre_completo} 👋")
        st.markdown("---")
        
        # --- Este es tu nuevo menú ---
        st.page_link("sistemaR.py", label="Dashboard Principal", icon="📊")
        st.page_link("pages/administracion.py", label="Administración", icon="👥")
        st.page_link("pages/recibos.py", label="Recibos de Pago", icon="🧾")
        st.page_link("pages/Historial.py", label="Historial de Grupos", icon="📚")
        # --- Fin del menú ---
        
        st.markdown("---")
        
        if st.button("Cerrar Sesión", use_container_width=True, type="primary"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.nombre_completo = None
            st.rerun()
            
    # --- CONTENIDO DEL DASHBOARD (Tu código de métricas) ---
    st.title("Dashboard Principal 🎓")
    st.markdown("---")
    st.subheader("Resumen General del Sistema")

    try:
        col1, col2, col3, col4 = st.columns(4)
        conn = get_connection()

        # ... (Tu código de métricas va aquí, no necesita cambios) ...
        query_alumnos = "SELECT COUNT(*) FROM Alumnos WHERE status_alumno = 'Activo'"
        total_alumnos = pd.read_sql(query_alumnos, conn).iloc[0,0]
        col1.metric(label="Alumnos Activos 🧑‍🎓", value=total_alumnos)

        query_ingresos = """
            SELECT SUM(monto) FROM Pagos 
            WHERE EXTRACT(MONTH FROM fecha_pago) = EXTRACT(MONTH FROM NOW()) 
              AND EXTRACT(YEAR FROM fecha_pago) = EXTRACT(YEAR FROM NOW())
        """
        ingresos = pd.read_sql(query_ingresos, conn).iloc[0,0]
        ingresos = ingresos if ingresos is not None else 0
        col2.metric(label="Ingresos del Mes 💵", value=f"${float(ingresos):,.2f}")

        query_grupos = "SELECT COUNT(*) FROM Grupos WHERE status_grupo = 'Activo'"
        total_grupos = pd.read_sql(query_grupos, conn).iloc[0,0]
        col3.metric(label="Grupos Activos 📚", value=total_grupos)

        query_pendientes = "SELECT SUM(monto) FROM Pagos WHERE status_pago = 'Pendiente'"
        pendientes = pd.read_sql(query_pendientes, conn).iloc[0,0]
        pendientes = pendientes if pendientes is not None else 0
        col4.metric(label="Monto Pendiente ⏳", value=f"${float(pendientes):,.2f}")

    except Exception as e:
        st.error(f"🔴 No se pudo cargar el resumen del dashboard. Error: {e}")