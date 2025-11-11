import streamlit as st
import psycopg2
import pandas as pd
import datetime
import bcrypt


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


st.markdown("""<script>document.querySelector('html').setAttribute('lang', 'es');</script>""", unsafe_allow_html=True)

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
    except Exception as e:
        # st.error(f"Error al verificar: {e}") # Descomentar para depurar
        st.error("Error de conexión al intentar verificar. Intente de nuevo.")
        st.cache_resource.clear() # Forzar reconexión
        return None

# --- (NUEVO) MODAL PARA MOSTRAR CUMPLEAÑEROS ---
@st.dialog("🎂 ¡Feliz Cumpleaños!")
def modal_cumpleaneros(df_cumpleaneros):
    st.markdown(f"#### ¡Felicidades a los siguientes alumnos por su cumpleaños!")
    st.write("") # Espacio
    
    for index, row in df_cumpleaneros.iterrows():
        # Calculamos la edad
        today = datetime.date.today()
        edad = today.year - row['fecha_nacimiento'].year - ((today.month, today.day) < (row['fecha_nacimiento'].month, row['fecha_nacimiento'].day))
        
        st.markdown(f"**🧑‍🎓 {row['nombre_completo']}** (cumple {edad} años)")
    
    st.write("") # Espacio
    if st.button("Cerrar", use_container_width=True, type="primary"):
        st.rerun()

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
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.nombre_completo = None
        st.session_state.show_timeout_message = True
        st.rerun()
    else:
        st.session_state.last_activity = now

# --- 2. SI NO HA HECHO LOGIN (Mostrar solo el formulario) ---
if not st.session_state.logged_in:
    
    st.set_page_config(page_title="Inicio de Sesión", layout="centered", initial_sidebar_state="collapsed")
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { display: none; }
            button[kind="primaryFormSubmit"] {
                background-color: #000896 !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.5rem 1rem !important;
                font-weight: 600 !important;
                transition: all 0.2s ease !important;
            }
            button[kind="primaryFormSubmit"]:hover {
                background-color: #00067A !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    st.title("Sistema de Gestión 🔑")
    
    # Mostrar mensaje de timeout si existe
    if hasattr(st.session_state, 'show_timeout_message') and st.session_state.show_timeout_message:
        st.error("🕒 Tu sesión ha expirado por inactividad. Por favor, inicia sesión nuevamente.")
        del st.session_state.show_timeout_message
    
    st.subheader("Por favor, inicia sesión para continuar")

    st.markdown('<div class="login-form-container">', unsafe_allow_html=True)
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Ingresar", type="primary")
        
        if submitted:
            nombre_usuario = check_login(username, password) 
            
            if nombre_usuario:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.nombre_completo = nombre_usuario
                st.session_state.last_activity = datetime.datetime.now()
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. SI SÍ HIZO LOGIN (Mostrar la app completa) ---
else:
    # Configuración de la página principal
    st.set_page_config(
        page_title="Dashboard Principal",
        layout="wide"
    )
    # (NOTA: La vieja llamada a 'load_css()' ha sido eliminada de aquí)

    # --- Menú lateral (Sidebar) ---
    with st.sidebar:
        st.title(f"Bienvenido, {st.session_state.nombre_completo} 👋")
        st.markdown("---")
        
        st.page_link("sistemaR.py", label="Dashboard Principal", icon="📊")
        st.page_link("pages/administracion.py", label="Administración", icon="👥")
        st.page_link("pages/recibos.py", label="Recibos de Pago", icon="🧾")
        st.page_link("pages/Historial.py", label="Historial de Grupos", icon="📚")
        st.page_link("pages/metricas.py", label="Métricas Históricas", icon="📈")
        show_theme_toggle()
        st.markdown("---")
        
        # (NOTA: El 'st.toggle' duplicado ha sido eliminado de aquí)
        # La función 'apply_theme_and_toggle()' ya lo añade en este lugar.
        
        if st.button("Cerrar Sesión", use_container_width=True, type="primary"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.nombre_completo = None
            st.rerun()
            
    # --- CONTENIDO DEL DASHBOARD (MÉTRICAS MEJORADAS) ---
    st.markdown(f"""
    <div class="main-header">
        <h1>Dashboard Principal 🎓</h1>
        <p>Vista general del sistema de gestión</p>
        <p style="text-align: center; font-size: 1.2rem; color: orange;">Mes Actual: {datetime.date.today().strftime('%B %Y')}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Resumen General del Sistema")

    try:
        conn = get_connection()
        
        # --- (NUEVO) Consulta de Cumpleaños (más eficiente) ---
        query_cumpleaneros = """
            SELECT nombre_completo, fecha_nacimiento 
            FROM Alumnos 
            WHERE status_alumno = 'Activo' 
            AND EXTRACT(MONTH FROM fecha_nacimiento) = EXTRACT(MONTH FROM CURRENT_DATE) 
            AND EXTRACT(DAY FROM fecha_nacimiento) = EXTRACT(DAY FROM CURRENT_DATE);
        """
        df_cumpleaneros = pd.read_sql(query_cumpleaneros, conn)
        total_cumpleaneros = len(df_cumpleaneros)

        # --- (MEJORADO) Métrica de Alumnos ---
        query_alumnos = "SELECT COUNT(*) FROM Alumnos WHERE status_alumno = 'Activo'"
        total_alumnos = pd.read_sql(query_alumnos, conn).iloc[0,0]
        
        # --- (MEJORADO) Métrica de Ingresos ---
        query_ingresos = """
            SELECT SUM(monto) FROM Pagos 
            WHERE EXTRACT(MONTH FROM fecha_pago) = EXTRACT(MONTH FROM NOW()) 
              AND EXTRACT(YEAR FROM fecha_pago) = EXTRACT(YEAR FROM NOW())
        """
        ingresos = pd.read_sql(query_ingresos, conn).iloc[0,0]
        ingresos = ingresos if ingresos is not None else 0
        
        # --- (MEJORADO) Métrica de Grupos ---
        query_grupos = "SELECT COUNT(*) FROM Grupos WHERE status_grupo = 'Activo'"
        total_grupos = pd.read_sql(query_grupos, conn).iloc[0,0]

        # --- (NUEVO) Diseño de Métricas con Tarjetas ---
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            with st.container(border=True):
                st.markdown("##### 🧑‍🎓 Alumnos Activos")
                st.markdown(f"<h1 style='text-align: center; color: #0d47a1;'>{total_alumnos}</h1>", unsafe_allow_html=True)
                # (NUEVO) Placeholder para alinear con el botón
                st.write('<div style="height: 38px;"></div>', unsafe_allow_html=True)

        with col2:
            with st.container(border=True):
                st.markdown("##### 💵 Ingresos del Mes")
                st.markdown(f"<h1 style='text-align: center; color: #28a745;'>${float(ingresos):,.2f}</h1>", unsafe_allow_html=True)
                # (NUEVO) Placeholder para alinear con el botón
                st.write('<div style="height: 38px;"></div>', unsafe_allow_html=True)

        with col3:
            with st.container(border=True):
                st.markdown("##### 📚 Grupos Activos")
                st.markdown(f"<h1 style='text-align: center; color: #0d47a1;'>{total_grupos}</h1>", unsafe_allow_html=True)
                # (NUEVO) Placeholder para alinear con el botón
                st.write('<div style="height: 38px;"></div>', unsafe_allow_html=True)
        
        with col4:
            # --- (NUEVO) Tarjeta de Cumpleaños ---
            with st.container(border=True):
                st.markdown("##### 🎂 Cumpleañeros de Hoy")
                st.markdown(f"<h1 style='text-align: center; color: #FF8400;'>{total_cumpleaneros}</h1>", unsafe_allow_html=True)
                
                # Si hay cumpleañeros, muestra el botón
                if total_cumpleaneros > 0:
                    if st.button("Ver Lista 🥳", key="ver_cumples", use_container_width=True, type="primary"):
                        modal_cumpleaneros(df_cumpleaneros)
                else:
                    # (NUEVO) Placeholder para alinear con el botón
                    st.write('<div style="height: 58px;"></div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"🔴 No se pudo cargar el resumen del dashboard. Error: {e}")