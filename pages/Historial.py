import streamlit as st
import pandas as pd
import psycopg2
import json

from utils.css import load_css
load_css()
# --- INICIO DEL BLOQUE "PORTERO" (Versión 2.0) ---

# 1. Sistema de timeout y verificación de sesión
import datetime as dt

if "last_activity" not in st.session_state:
    st.session_state.last_activity = dt.datetime.now()

if "session_timeout_minutes" not in st.session_state:
    st.session_state.session_timeout_minutes = 60

# Verificar si el usuario ha iniciado sesión y no ha expirado la sesión
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.set_page_config(page_title="Acceso Denegado", layout="centered")
    
    # Ocultar sidebar completamente
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.warning("🔒 Por favor, inicia sesión para ver esta página.")
    st.page_link("sistemaR.py", label="Ir a la página de Login", icon="🔑")
    st.stop()

# Verificar timeout
if st.session_state.logged_in:
    now = dt.datetime.now()
    time_since_activity = (now - st.session_state.last_activity).total_seconds() / 60
    
    if time_since_activity > st.session_state.session_timeout_minutes:
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.nombre_completo = None
        st.session_state.show_timeout_message = True
        # Forzar redirección
        st.switch_page("sistemaR.py")
    else:
        st.session_state.last_activity = now

# 2. Si el usuario SÍ está logueado, mostrar el menú y el botón de logout
with st.sidebar:
    st.title(f"Bienvenido, {st.session_state.nombre_completo} 👋")
    st.markdown("---")
    
    # --- El mismo menú bonito ---
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
        st.page_link("sistemaR.py", label="Ir a Login", icon="🔑") # Te redirige
        st.rerun()
        
# --- FIN DEL BLOQUE "PORTERO" ---

st.set_page_config(page_title="Historial de Grupos", layout="wide")
st.title("🗂️ Historial de Grupos Finalizados")
load_css()
# --- LÓGICA DE CONEXIÓN ROBUSTA ---
@st.cache_resource
def init_connection():
    return psycopg2.connect(st.secrets["DB_CONNECTION_STRING"])

def get_connection():
    conn = init_connection()
    try:
        conn.cursor().execute("SELECT 1")
    except (psycopg2.InterfaceError, psycopg2.OperationalError, psycopg2.errors.InFailedSqlTransaction):
        if not conn.closed:
            conn.rollback()
        st.cache_resource.clear()
        conn = init_connection()
    return conn

# --- LÓGICA PARA MOSTRAR EL HISTORIAL (CORREGIDA) ---
try:
    conn = get_connection()
    # Usamos fecha_termino para ordenar, ya que es la columna de la fecha principal de archivado
    query = "SELECT * FROM Grupos_Historial ORDER BY fecha_termino DESC"
    df_historial = pd.read_sql(query, conn)

    if df_historial.empty:
        st.info("No hay grupos archivados en el historial.")
    else:
        st.subheader("Grupos Archivados")
        for index, row in df_historial.iterrows():
            
            # Formateamos la fecha de archivado para el título
            if pd.notna(row['fecha_termino']):
                fecha_archivado = row['fecha_termino'].strftime('%d de %B de %Y')
            else:
                fecha_archivado = "Fecha no registrada"
            
            with st.expander(f"**Grupo: {row['nombre_grupo']}** (Archivado el {fecha_archivado})"):
                
                # --- CORRECCIÓN CLAVE AQUÍ ---
                # Leemos las fechas directamente de sus columnas en la tabla, no del JSON
                fecha_inicio = row['fecha_inicio'].strftime('%Y-%m-%d') if pd.notna(row['fecha_inicio']) else "N/A"
                fecha_termino_grupo = row['fecha_termino'].strftime('%Y-%m-%d') if pd.notna(row['fecha_termino']) else "N/A"

                # Mostramos los datos en columnas para un mejor diseño
                col1, col2, col3 = st.columns(3)
                col1.write(f"**Profesor:** {row['nombre_profesor']}")
                col2.write(f"**Fecha de Inicio del Grupo:** {fecha_inicio}")
                col3.write(f"**Fecha de Término del Grupo:** {fecha_termino_grupo}")
                
                st.write("**Alumnos en este grupo:**")
                
                try:
                    datos_snapshot = row['datos_grupo_alumnos'] if row['datos_grupo_alumnos'] else {}
                    if datos_snapshot and 'alumnos' in datos_snapshot:
                        alumnos_data = datos_snapshot['alumnos']
                        if alumnos_data:
                            df_alumnos = pd.DataFrame(alumnos_data)
                            st.dataframe(df_alumnos, use_container_width=True)
                        else:
                            st.write("No se registraron alumnos en este grupo.")
                    else:
                        st.write("No hay datos de alumnos guardados para este grupo.")
                except Exception as e:
                    st.error(f"No se pudieron cargar los datos de los alumnos para este grupo. Error: {e}")

except Exception as e:
    st.error(f"Error al cargar el historial de grupos: {e}")