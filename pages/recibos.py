import streamlit as st
import psycopg2
import pandas as pd
import datetime
import base64
import io
from fpdf import FPDF
from num2words import num2words

# (Importante: Asumo que 'streamlit_keyup' ya NO es necesario,
# ya que tu 'administracion.py' usa un st.button + st.text_input)
from utils.css import load_css

# --- CONFIGURACIÓN Y CSS ---
# st.set_page_config debe ser lo primero, pero solo UNA VEZ por script.
# La llamada en 'sistemaR.py' es la principal.
# Aquí solo llamamos a load_css()
load_css()

# --- INICIO DEL BLOQUE "PORTERO" (Versión 2.0) ---

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
    # --- Fin del menú ---
    
    st.markdown("---")
    
    if st.button("Cerrar Sesión", use_container_width=True, type="primary"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.nombre_completo = None
        st.page_link("sistemaR.py", label="Ir a Login", icon="🔑") # Te redirige
        st.rerun()
        
# --- FIN DEL BLOQUE "PORTERO" ---

# --- INICIO DE LA PÁGINA DE RECIBOS ---

# (st.set_page_config ya no va aquí, se maneja arriba o en la app principal)
st.markdown("""
<div class="main-header">
    <h1>Registro de Pagos y Recibos 🧾</h1>
    <p>Gestiona los pagos y recibos del sistema</p>
</div>
""", unsafe_allow_html=True)
# (load_css() ya se llamó al inicio)

# --- LÓGICA DE CONEXIÓN ROBUSTA ---
@st.cache_resource
def init_connection():
    return psycopg2.connect(st.secrets["DB_CONNECTION_STRING"])

def get_connection():
    conn = init_connection()
    try:
        # Hacemos una consulta rápida para probar si la conexión está "viva"
        conn.cursor().execute("SELECT 1")
    except (psycopg2.InterfaceError, psycopg2.OperationalError, psycopg2.errors.InFailedSqlTransaction):
        # Si hay un error, hacer rollback y limpiar la caché
        if not conn.closed:
            try:
                if conn.status == psycopg2.extensions.STATUS_IN_TRANSACTION:
                    conn.rollback()
            except Exception:
                pass # Ignorar errores en rollback
        st.cache_resource.clear()
        conn = init_connection()
    return conn

# --- FUNCIONES AUXILIARES ---
def numero_a_letra(numero):
    try:
        entero = int(numero)
        decimal = int(round((numero - entero) * 100))
        texto_entero = num2words(entero, lang='es').upper()
        return f"{texto_entero} PESOS {decimal:02d}/100 M.N."
    except Exception:
        return "CANTIDAD INVÁLIDA"

def generar_recibo_pdf(folio, fecha, nombre_alumno, concepto, monto, metodo_pago):
    pdf = FPDF()
    pdf.add_page()
    
    # Título principal (AHORA VA PRIMERO)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Recibo de pago', 0, 1, 'C')
    pdf.ln(5) # Un pequeño espacio

    # --- IMÁGENES DEL ENCABEZADO (AJUSTADAS) ---
    try:
        # 1. Logo principal más grande (w=80) y centrado
        pdf.image('utils/logo_principal.jpg', x=65, y=pdf.get_y(), w=80)
        pdf.ln(20) # Más espacio después del logo
        
        # 2. Barra de contacto más ancha y centrada
        pdf.image('utils/info_contacto.png', x=30, y=pdf.get_y(), w=150)
        pdf.ln(15) # Más espacio después de la barra de contacto

    except Exception: # Captura cualquier error de imagen
        st.warning("No se encontraron las imágenes del logo/contacto.")
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 5, "CARPE DIEM MÉXICO", 0, 1, 'C')
        pdf.ln(20)


    # --- DATOS DEL RECIBO CON COLORES ---
    # Establecemos el color azul para las etiquetas
    pdf.set_text_color(70, 130, 180) 
    pdf.set_font('Arial', 'B', 12)
    
    # Fecha y Folio
    pdf.cell(15, 10, 'Fecha:', 0, 0)
    pdf.set_text_color(0, 0, 0) # Volvemos a negro para el dato
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, fecha.strftime('%d / %m / %Y'), 0, 1)

    pdf.set_text_color(70, 130, 180)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(15, 10, 'Folio:', 0, 0)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, str(folio), 0, 1)
    pdf.ln(5)
    
    # Datos del pago
    pdf.set_text_color(70, 130, 180)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(28, 10, 'Recibí de:', 0, 0)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 12) # El nombre en negrita
    pdf.cell(0, 10, nombre_alumno.upper(), 0, 1)
    
    pdf.set_text_color(70, 130, 180)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(38, 10, 'La cantidad de:', 0, 0)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 12) # El monto en normal
    pdf.cell(0, 10, f"${float(monto):,.2f} ({numero_a_letra(float(monto))})", 0, 1)
    
    pdf.set_text_color(70, 130, 180)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(42, 10, 'Por concepto de:', 0, 0)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 12) # El concepto en normal
    pdf.cell(0, 10, concepto.upper(), 0, 1)
    
    # --- FIRMA ---
    pdf.ln(25)
    try:
        # Cargar firma desde Streamlit Secrets (Base64 encriptada)
        firma_base64 = st.secrets["FIRMA_BASE64"]
        firma_data = base64.b64decode(firma_base64)
        firma_stream = io.BytesIO(firma_data)
        
        # Insertar la firma en el PDF
        pdf.image(firma_stream, x=80, y=pdf.get_y(), w=50)
        pdf.ln(15)
    except (KeyError, Exception):
        # Si no hay firma en los secrets, solo saltar la línea
        pdf.ln(15)

    pdf.cell(0, 1, '_________________________________', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'MARA GRACIELA RODRIGUEZ ORTIZ', 0, 1, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, 'Recibí de conformidad', 0, 1, 'C')
    
    return bytes(pdf.output())

# --- FORMULARIO PARA REGISTRAR PAGO ---

# (SOLUCIÓN 1: 'expanded' cambiado a False)
with st.expander("Registrar Nuevo Pago y Generar Recibo", expanded=False):
    conn = get_connection()
    st.write("")
    # --- Filtro por Grupo ---
    df_grupos = pd.read_sql("SELECT grupo_id, nombre_grupo FROM Grupos WHERE status_grupo = 'Activo' ORDER BY nombre_grupo ASC", conn)
    opciones_grupos = {0: "Todos los Grupos"}
    for index, row in df_grupos.iterrows():
        opciones_grupos[row['grupo_id']] = row['nombre_grupo']

    grupo_filtrado_id = st.selectbox(
        "Filtrar por Grupo",
        options=list(opciones_grupos.keys()),
        format_func=lambda x: opciones_grupos[x]
    )
    
    st.write("")
    # Carga de alumnos según el filtro
    if grupo_filtrado_id == 0:
        df_alumnos_filtrados = pd.read_sql("SELECT alumno_id, nombre_completo FROM Alumnos WHERE status_alumno = 'Activo' ORDER BY nombre_completo ASC", conn)
    else:
        query_alumnos_filtrados = "SELECT a.alumno_id, a.nombre_completo FROM Alumnos a JOIN Inscripciones i ON a.alumno_id = i.alumno_id WHERE a.status_alumno = 'Activo' AND i.grupo_id = %s ORDER BY a.nombre_completo ASC;"
        df_alumnos_filtrados = pd.read_sql(query_alumnos_filtrados, conn, params=(grupo_filtrado_id,))

    if df_alumnos_filtrados.empty:
        st.warning("No hay alumnos 'Activos' que coincidan con el filtro seleccionado.")
    else:
        # --- ESTRUCTURA CORREGIDA A PRUEBA DE ERRORES ---
        
        # 1. SELECCIONAMOS AL ALUMNO FUERA DEL FORMULARIO
        alumno_id = st.selectbox(
            "Selecciona un Alumno",
            options=df_alumnos_filtrados['alumno_id'],
            format_func=lambda x: df_alumnos_filtrados[df_alumnos_filtrados['alumno_id'] == x]['nombre_completo'].values[0],
            index=None,
            placeholder="Selecciona un alumno..."
        )
        
        # 2. CALCULAMOS LOS CONCEPTOS DISPONIBLES
        conceptos_disponibles = []
        if alumno_id:
            todos_conceptos = ["Inscripción", "Mensualidad 1", "Mensualidad 2", "Mensualidad 3", "Mensualidad 4", "Mensualidad 5", "Mensualidad 6"]
            query_pagados = "SELECT p.concepto FROM Pagos p JOIN Inscripciones i ON p.inscripcion_id = i.inscripcion_id WHERE i.alumno_id = %s"
            df_pagados = pd.read_sql(query_pagados, conn, params=(alumno_id,))

            if df_pagados.empty:
                conceptos_disponibles = todos_conceptos
            else:
                conceptos_pagados = list(df_pagados['concepto'].str.strip())
                conceptos_disponibles = [c for c in todos_conceptos if c not in conceptos_pagados]
        
        # 3. DIBUJAMOS EL FORMULARIO CON LOS DATOS YA CALCULADOS
        with st.form("registro_pago_form"):
            # Mostramos el nombre del alumno seleccionado dentro del form para claridad
            if alumno_id:
                st.write(f"**Alumno Seleccionado:** {df_alumnos_filtrados[df_alumnos_filtrados['alumno_id'] == alumno_id]['nombre_completo'].values[0]}")
            
            col1, col2 = st.columns(2)
            with col1:
                concepto = st.selectbox("Concepto del Pago", options=conceptos_disponibles, disabled=(not alumno_id))
                monto = st.number_input("Monto Pagado", min_value=0.0, step=50.0, value=0.0)

            with col2:
                metodo = st.selectbox("Método de Pago", ["Transferencia", "Efectivo", "Tarjeta"])
                fecha = st.date_input("Fecha del Pago", value=datetime.date.today())
            
            if alumno_id and not conceptos_disponibles:
                st.info("Este alumno ya ha completado todos sus pagos.")

            
            # Botón de envío (tipo 'primary' para que sea azul)
            submitted = st.form_submit_button(
                "Registrar Pago", 
                disabled=(not conceptos_disponibles or not alumno_id),
                type="primary"
            )
            
            if submitted:
                if not alumno_id or not concepto:
                    st.error("Por favor, selecciona un alumno y un concepto de pago.")
                else:
                    try:
                        with conn.cursor() as cur:
                            cur.execute("SELECT inscripcion_id FROM Inscripciones WHERE alumno_id = %s LIMIT 1", (alumno_id,))
                            res = cur.fetchone()
                            if not res:
                                st.error("Este alumno no tiene una inscripción activa.")
                                st.stop()
                            inscripcion_id = res[0]
                            
                            cur.execute("SELECT MAX(folio) FROM Pagos")
                            max_folio = cur.fetchone()[0]
                            nuevo_folio = (max_folio + 1) if max_folio is not None else 1001
                            
                            sql = "INSERT INTO Pagos (inscripcion_id, folio, monto, fecha_pago, concepto, metodo_pago, status_pago) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                            cur.execute(sql, (inscripcion_id, str(nuevo_folio), monto, fecha, concepto, metodo, 'Completo'))
                            conn.commit()
                            st.success(f"¡Pago registrado con folio {nuevo_folio}!")
                            st.rerun() # Esto recargará la página (y el expander se quedará cerrado)
                    except Exception as e:
                        st.error(f"Ocurrió un error: {e}")

# --- BOTÓN DE DESCARGA ---
if 'pdf_a_descargar' in st.session_state:
    st.download_button(
        label="✅ Descargar Recibo Generado", 
        data=st.session_state.pdf_a_descargar["data"],
        file_name=st.session_state.pdf_a_descargar["file_name"]
    )
    del st.session_state.pdf_a_descargar


# --- TABLA DE HISTORIAL DE PAGOS (SOLUCIÓN 2 y 3) ---
# 1. Envolvemos todo en el st.container(border=True) para la "tarjeta"
with st.container(border=True):
    st.subheader("Historial de Pagos Registrados")

    # 2. Replicamos la estructura de búsqueda de admin.py
    col_search_button, col_search_input = st.columns([0.1, 0.9])
    
    with col_search_input:
        search_term_input = st.text_input(
            "Buscar por Folio o Nombre",
            placeholder="Buscar por Folio o Nombre...",
            key="search_pagos_realtime", # Key para el input
            value=st.session_state.get("search_value_pagos", ""), # Valor guardado
            label_visibility="collapsed" # Ocultamos la etiqueta
        )

    # El filtro se basa en el valor guardado en session_state
    search_term = st.session_state.get("search_value_pagos", "")

    with col_search_button:
        if st.button("🔍", key="search_pagos_button", use_container_width=True):
            # Al hacer clic, se actualiza el valor guardado y se recarga
            st.session_state["search_value_pagos"] = st.session_state["search_pagos_realtime"]
            st.rerun()

    # (Si el valor del input cambia y se presiona Enter, también se filtra)
    if search_term_input != search_term:
        st.session_state.search_value_pagos = search_term_input
        search_term = search_term_input
        # No es necesario st.rerun() aquí, Streamlit lo maneja al presionar Enter

    # Divisor

    try:
        conn = get_connection()
        query_pagos = """
            SELECT p.folio, a.nombre_completo, p.metodo_pago, p.fecha_pago, 
                   p.monto, p.concepto, p.status_pago
            FROM Pagos p
            JOIN Inscripciones i ON p.inscripcion_id = i.inscripcion_id
            JOIN Alumnos a ON i.alumno_id = a.alumno_id
            ORDER BY p.folio DESC;
        """
        df_pagos = pd.read_sql(query_pagos, conn)
        df_pagos["folio"] = df_pagos["folio"].astype(str)

        # Aplicar el filtro si 'search_term' (el confirmado) existe
        if search_term and search_term.strip():
            search_term_clean = search_term.strip()
            df_pagos = df_pagos[
                df_pagos['folio'].str.contains(search_term_clean, case=False) |
                df_pagos['nombre_completo'].str.contains(search_term_clean, case=False)
            ]
        
        # --- NUEVA ESTRUCTURA DE TABLA (SOLUCIÓN 3) ---
        
        # 3. Envolvemos la tabla en el div que tu CSS espera
        st.markdown('<div class="table-container">', unsafe_allow_html=True)

        col_widths = [2, 2, 3.5, 2, 2, 1.5, 3, 2]
        headers = ["Recibo", "Folio", "Nombre", "Método de Pago", "Fecha", "Monto", "Concepto", "Status"]

        # 4. Creamos la CABECERA con st.container(border=True)
        with st.container(border=True):
            cols_header = st.columns(col_widths)
            for col, header in zip(cols_header, headers):
                col.markdown(f"**{header}**")

        # 5. Creamos las FILAS con st.container(border=True)
        if df_pagos.empty:
            st.info("No se encontraron pagos con ese filtro.")
        else:
            for _, row in df_pagos.iterrows():
                with st.container(border=True):
                    cols_row = st.columns(col_widths)
                    
                    # Botón Generar (SOLUCIÓN 4: con estilo 'btn-warning')
                    with cols_row[0]:
                        st.markdown('<div class="btn-warning">', unsafe_allow_html=True)
                        if st.button("📄 Generar", key=f"pdf_{row['folio']}", use_container_width=True):
                            pdf_bytes = generar_recibo_pdf(
                                row['folio'], row['fecha_pago'], row['nombre_completo'],
                                row['concepto'], row['monto'], row['metodo_pago']
                            )
                            st.session_state.pdf_a_descargar = {"data": pdf_bytes, "file_name": f"recibo_{row['folio']}.pdf"}
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Folio
                    cols_row[1].markdown(f"<span style='color: #1c83e1; font-weight: bold;'>{row['folio']}</span>", unsafe_allow_html=True)
                    
                    # Resto de los datos
                    cols_row[2].write(row['nombre_completo'])
                    cols_row[3].write(row['metodo_pago'])
                    cols_row[4].write(row['fecha_pago'].strftime('%d/%m/%Y'))
                    cols_row[5].write(f"${float(row['monto']):,.2f}")
                    cols_row[6].write(row['concepto'])
                    cols_row[7].write(row['status_pago'])

        # 6. Cerramos el div del contenedor
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Ocurrió un error al cargar el historial de pagos: {e}")

# (El 'except' de arriba cierra el 'try' de la tabla)
# (Este 'with' cierra el st.container(border=True) principal)