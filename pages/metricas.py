import streamlit as st
import psycopg2
import pandas as pd
import datetime

# --- (CORREGIDO) PASO 1: IMPORTAR LÓGICA DE TEMA ---
try:
    # ¡Importamos AMBAS funciones!
    from utils.theme import apply_theme, show_theme_toggle 
except ImportError:
    # Este error ahora SÍ significa que el archivo __init__.py falta
    st.error("Error: No se pudo encontrar 'utils/theme.py'. ¿Añadiste el archivo 'utils/__init__.py'?")
    st.stop()

# --- (CORREGIDO) PASO 2: APLICAR EL TEMA ---
# Esta función SOLO carga el CSS
apply_theme()

# --- INICIO DEL BLOQUE "PORTERO" ---

# 1. Sistema de timeout y verificación de sesión
if "last_activity" not in st.session_state:
    st.session_state.last_activity = datetime.datetime.now()

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
    now = datetime.datetime.now()
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
    st.page_link("pages/metricas.py", label="Métricas Históricas", icon="📈")
    show_theme_toggle()
    
    st.markdown("---")
    
    if st.button("Cerrar Sesión", use_container_width=True, type="primary"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.nombre_completo = None
        st.page_link("sistemaR.py", label="Ir a Login", icon="🔑") # Te redirige
        st.rerun()
        
# --- FIN DEL BLOQUE "PORTERO" ---

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
            try:
                if conn.status == psycopg2.extensions.STATUS_IN_TRANSACTION:
                    conn.rollback()
            except Exception:
                pass # Ignorar errores en rollback
        st.cache_resource.clear()
        conn = init_connection()
    return conn

# --- CONTENIDO DE LA PÁGINA DE MÉTRICAS ---
st.markdown("""
<div class="main-header">
    <h1>Métricas Históricas 📈</h1>
    <p>Análisis de ingresos y registros de alumnos a lo largo del tiempo</p>
</div>
""", unsafe_allow_html=True)

# --- TABS PRINCIPALES ---
tab_ingresos, tab_alumnos = st.tabs([" Ingresos Mensuales", " Alumnos Mensuales"])

with tab_ingresos:
    st.subheader("Ingresos Mensuales")

    @st.cache_data(ttl=600)
    def get_ingresos_mensuales():
        conn = get_connection()
        # --- 💡 CAMBIO 1: Alias de SQL actualizados ---
        query = """
            SELECT 
                TO_CHAR(fecha_pago, 'YYYY-MM') AS "Fecha",
                SUM(monto) AS "Ingresos"
            FROM Pagos
            GROUP BY "Fecha"
            ORDER BY "Fecha";
        """
        df_ingresos = pd.read_sql(query, conn)
        return df_ingresos

    df_ingresos_mensuales = get_ingresos_mensuales()
    años = sorted(list({f[:4] for f in df_ingresos_mensuales["Fecha"]}), reverse=True)
    meses_nombres = [
        "Todos los meses","Enero","Febrero","Marzo","Abril","Mayo","Junio",
        "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
    ]
    meses_map = {
        "Enero":"01","Febrero":"02","Marzo":"03","Abril":"04","Mayo":"05","Junio":"06",
        "Julio":"07","Agosto":"08","Septiembre":"09","Octubre":"10","Noviembre":"11","Diciembre":"12"
    }
    c1, c2 = st.columns(2)
    with c1:
        año_sel = st.selectbox("Año", options=["Todos los años"] + años, index=0, key="ingresos_ano")
    with c2:
        mes_sel = st.selectbox("Mes", options=meses_nombres, index=0, key="ingresos_mes")
    df_ingresos_filtrado = df_ingresos_mensuales
    if año_sel != "Todos los años":
        df_ingresos_filtrado = df_ingresos_filtrado[df_ingresos_filtrado["Fecha"].str.slice(0,4) == str(año_sel)]
    if mes_sel != "Todos los meses":
        df_ingresos_filtrado = df_ingresos_filtrado[df_ingresos_filtrado["Fecha"].str.slice(5,7) == meses_map[mes_sel]]

    # Convertir el DataFrame a HTML con una clase CSS y sin el índice
    df_html_ingresos = df_ingresos_filtrado.to_html(
        index=False, 
        classes="tabla-estilizada",
        justify="left"               
    )
    st.markdown(df_html_ingresos, unsafe_allow_html=True)


with tab_alumnos:
    st.subheader("Alumnos Registrados Mensualmente")

    @st.cache_data(ttl=600)
    def get_alumnos_registrados_mensuales():
        conn = get_connection()
        # --- 💡 CAMBIO 2: Alias de SQL actualizados ---
        query = """
            SELECT 
                TO_CHAR(g.fecha_inicio, 'YYYY-MM') AS "Fecha",
                COUNT(i.alumno_id) AS "Alumnos Registrados"
            FROM Inscripciones i
            JOIN Grupos g ON i.grupo_id = g.grupo_id
            GROUP BY "Fecha"
            ORDER BY "Fecha";
        """
        df_alumnos = pd.read_sql(query, conn)
        return df_alumnos

    df_alumnos_registrados_mensuales = get_alumnos_registrados_mensuales()
    años_a = sorted(list({f[:4] for f in df_alumnos_registrados_mensuales["Fecha"]}), reverse=True)
    meses_nombres_a = [
        "Todos los meses","Enero","Febrero","Marzo","Abril","Mayo","Junio",
        "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
    ]
    meses_map_a = {
        "Enero":"01","Febrero":"02","Marzo":"03","Abril":"04","Mayo":"05","Junio":"06",
        "Julio":"07","Agosto":"08","Septiembre":"09","Octubre":"10","Noviembre":"11","Diciembre":"12"
    }
    c3, c4 = st.columns(2)
    with c3:
        año_sel_a = st.selectbox("Año", options=["Todos los años"] + años_a, index=0, key="alumnos_ano")
    with c4:
        mes_sel_a = st.selectbox("Mes", options=meses_nombres_a, index=0, key="alumnos_mes")
    df_alumnos_filtrado = df_alumnos_registrados_mensuales
    if año_sel_a != "Todos los años":
        df_alumnos_filtrado = df_alumnos_filtrado[df_alumnos_filtrado["Fecha"].str.slice(0,4) == str(año_sel_a)]
    if mes_sel_a != "Todos los meses":
        df_alumnos_filtrado = df_alumnos_filtrado[df_alumnos_filtrado["Fecha"].str.slice(5,7) == meses_map_a[mes_sel_a]]

    # Reutilizamos la misma clase CSS para la segunda tabla
    df_html_alumnos = df_alumnos_filtrado.to_html(
        index=False, 
        classes="tabla-estilizada",
        justify="left"
    )
    st.markdown(df_html_alumnos, unsafe_allow_html=True)
