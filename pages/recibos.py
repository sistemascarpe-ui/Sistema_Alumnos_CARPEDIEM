import streamlit as st
import psycopg2
import pandas as pd
import datetime
from fpdf import FPDF
from num2words import num2words

from utils.css import load_css
# --- INICIO DEL BLOQUE "PORTERO" (Versión 2.0) ---

# 1. Verificar si el usuario ha iniciado sesión
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Por favor, inicia sesión para ver esta página.")
    st.page_link("sistemaR.py", label="Ir a la página de Login", icon="🔑")
    st.stop()

# 2. Si el usuario SÍ está logueado, mostrar el menú y el botón de logout
with st.sidebar:
    st.title(f"Bienvenido, {st.session_state.nombre_completo} 👋")
    st.markdown("---")
    
    # --- El mismo menú bonito ---
    st.page_link("sistemaR.py", label="Dashboard Principal", icon="📊")
    st.page_link("pages/administracion.py", label="Administración", icon="👥")
    st.page_link("pages/recibos.py", label="Recibos de Pago", icon="🧾")
    st.page_link("pages/historial.py", label="Historial de Grupos", icon="📚")
    # --- Fin del menú ---
    
    st.markdown("---")
    
    if st.button("Cerrar Sesión", use_container_width=True, type="primary"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.nombre_completo = None
        st.page_link("sistemaR.py", label="Ir a Login", icon="🔑") # Te redirige
        st.rerun()
        
# --- FIN DEL BLOQUE "PORTERO" ---
st.set_page_config(page_title="Recibos", layout="wide")
st.title("Registro de Pagos y Recibos 🧾")


load_css()

# --- LÓGICA DE CONEXIÓN ROBUSTA ---
@st.cache_resource
def init_connection():
    return psycopg2.connect(st.secrets["DB_CONNECTION_STRING"])

def get_connection():
    conn = init_connection()
    try:
        # Hacemos una consulta rápida para probar si la conexión está "viva"
        conn.cursor().execute("SELECT 1")
    except (psycopg2.InterfaceError, psycopg2.OperationalError) as e:
        # Si la conexión está cerrada o rota, la restablecemos.
        st.cache_resource.clear()
        conn = init_connection()
    except psycopg2.errors.InFailedSqlTransaction:
        # --- AQUÍ ESTÁ LA CORRECCIÓN ---
        # Si la transacción anterior falló, la revertimos para poder continuar.
        conn.rollback()
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

    except FileNotFoundError:
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
        # 3. Ruta de tu imagen de la firma
        pdf.image('utils/firma.jpg', x=80, y=pdf.get_y(), w=50)
        pdf.ln(15) # Ajusta este valor para el espacio después de la firma
    except FileNotFoundError:
        st.warning("No se encontró la imagen de la firma.")
        pdf.ln(15)

    pdf.cell(0, 1, '_________________________________', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'MARA GRACIELA RODRIGUEZ ORTIZ', 0, 1, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, 'Recibí de conformidad', 0, 1, 'C')
    
    return bytes(pdf.output())

# --- FORMULARIO PARA REGISTRAR PAGO ---
with st.expander("Registrar Nuevo Pago y Generar Recibo", expanded=True):
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

            
            # Botón de envío
            submitted = st.form_submit_button("Registrar Pago", disabled=(not conceptos_disponibles or not alumno_id))
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
                            st.rerun()
                    except Exception as e:
                        st.error(f"Ocurrió un error: {e}")

# --- BOTÓN DE DESCARGA ---
if 'pdf_a_descargar' in st.session_state:
    st.download_button(label="✅ Descargar Recibo Generado", **st.session_state.pdf_a_descargar)
    del st.session_state.pdf_a_descargar

st.markdown("---")

# --- TABLA DE HISTORIAL DE PAGOS ---
st.subheader("Historial de Pagos Registrados")
try:
    conn = get_connection()
    # --- CONSULTA SIMPLIFICADA ---
    query_pagos = """
        SELECT p.folio, a.nombre_completo, p.metodo_pago, p.fecha_pago, 
               p.monto, p.concepto, p.status_pago
        FROM Pagos p
        JOIN Inscripciones i ON p.inscripcion_id = i.inscripcion_id
        JOIN Alumnos a ON i.alumno_id = a.alumno_id
        ORDER BY p.folio DESC;
    """
    df_pagos = pd.read_sql(query_pagos, conn)

    # Forzar a que el folio se muestre como texto en negro
    df_pagos["folio"] = df_pagos["folio"].astype(str)

    search_term = st.text_input("🔍 Buscar por Folio o Nombre", key="search_pagos")
    if search_term:
        df_pagos = df_pagos[
            df_pagos['folio'].str.contains(search_term, case=False) |
            df_pagos['nombre_completo'].str.contains(search_term, case=False)
        ]

    col_widths = [1.5, 2, 3.5, 2, 2, 1.5, 3, 2]
    headers = ["Recibo", "Folio", "Nombre", "Método de Pago", "Fecha", "Monto", "Concepto", "Status"]
    header_cols = st.columns(col_widths)
    for i, header in enumerate(headers):
        header_cols[i].markdown(f"**{header}**")
    st.markdown("<hr style='margin-top:0; margin-bottom:0'>", unsafe_allow_html=True)

    for i, row in df_pagos.iterrows():
        cols = st.columns(col_widths)
        if cols[0].button("📄 Generar", key=f"pdf_{row['folio']}", use_container_width=True):
            pdf_bytes = generar_recibo_pdf(
                row['folio'], row['fecha_pago'], row['nombre_completo'],
                row['concepto'], row['monto'], row['metodo_pago']
            )
            st.session_state.pdf_a_descargar = {"data": pdf_bytes, "file_name": f"recibo_{row['folio']}.pdf"}
            st.rerun()

        cols[1].markdown(f"<span style='color: #1c83e1; font-weight: bold;'>{row['folio']}</span>", unsafe_allow_html=True)
        cols[2].write(row['nombre_completo'])
        cols[3].write(row['metodo_pago'])
        cols[4].write(row['fecha_pago'].strftime('%d/%m/%Y'))
        cols[5].write(f"${float(row['monto']):,.2f}")
        cols[6].write(row['concepto'])
        cols[7].write(row['status_pago'])

except Exception as e:
    st.error(f"Ocurrió un error al cargar el historial de pagos: {e}")
