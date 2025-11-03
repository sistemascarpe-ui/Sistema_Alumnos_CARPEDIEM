import streamlit as st
import psycopg2
import pandas as pd
import datetime
import json


# Asumiendo que tienes utils.css
from utils.css import load_css

# --- CONFIGURACIÓN INICIAL Y CSS ---
# st.set_page_config debe ser lo primero y solo una vez
st.set_page_config(page_title="Administración", layout="wide")
load_css() # Cargar CSS una sola vez

# --- INICIO DEL BLOQUE "PORTERO" (Simplificado para páginas) ---
# 1. Verificar si el usuario ha iniciado sesión
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    # No es necesario ocultar sidebar aquí, se hace en sistemaR.py
    st.warning("🔒 Por favor, inicia sesión para ver esta página.")
    st.page_link("sistemaR.py", label="Ir a la página de Login", icon="🔑")
    st.stop() # Detener si no está logueado

# 2. Si está logueado, mostrar el menú y botón de logout
with st.sidebar:
    st.title(f"Bienvenido, {st.session_state.nombre_completo} 👋")
    st.markdown("---")
    
    # --- Menú bonito ---
    st.page_link("sistemaR.py", label="Dashboard Principal", icon="📊")
    st.page_link("pages/administracion.py", label="Administración", icon="👥")
    st.page_link("pages/recibos.py", label="Recibos de Pago", icon="🧾")
    # Asegúrate que el nombre del archivo sea Historial.py o historial.py
    st.page_link("pages/Historial.py", label="Historial de Grupos", icon="📚") 
    
    st.markdown("---")
    
    # Se usa type="primary" para que el CSS lo detecte (Botón Azul Sólido)
    if st.button("Cerrar Sesión", key="logout_admin", use_container_width=True, type="primary"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.nombre_completo = None
        st.rerun()
        
# --- FIN DEL BLOQUE "PORTERO" ---


# --- CONTENIDO DE LA PÁGINA DE ADMINISTRACIÓN ---

# Header principal
st.markdown("""
<div class="main-header">
    <h1> Administración del Sistema</h1>
    <p>Gestiona alumnos, grupos y profesores de manera eficiente</p>
</div>
""", unsafe_allow_html=True)

# --- CONEXIÓN A LA BD (Con Rollback) ---
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
                # Intenta hacer rollback solo si la transacción falló
                if conn.status == psycopg2.extensions.STATUS_IN_TRANSACTION:
                    conn.rollback()
            except Exception as rb_error:
                print(f"Error durante rollback: {rb_error}") # Log para debug
        st.cache_resource.clear()
        conn = init_connection()
    return conn

# --- FUNCIONES DE TABLA REFACTORIZADAS ---
def display_data_table(df, col_widths, headers, custom_renderers):
    import streamlit as st
    
    # Encabezado de la tabla
    with st.container(border=True):
        cols = st.columns(col_widths)
        for col, header in zip(cols, headers):
            col.markdown(f"**{header}**")

    # Filas del cuerpo
    for _, row in df.iterrows():
        with st.container(border=True):
            cols = st.columns(col_widths)
            for col, (header, renderer) in zip(cols, custom_renderers.items()):
                with col:
                    renderer(row)

# --- HANDLERS Y FUNCIONES DE MODAL ---
def handle_status_change(alumno_id):
    nuevo_status = st.session_state[f"status_{alumno_id}"]
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE Alumnos SET status_alumno = %s WHERE alumno_id = %s", (nuevo_status, int(alumno_id)))
            conn.commit()
        st.success(f"Status del alumno {alumno_id} actualizado a {nuevo_status}.")
        st.rerun()
    except Exception as e:
        st.error(f"Error al actualizar status: {e}")
        conn.rollback()

def handle_certificado_change(alumno_id):
    nuevo_certificado = st.session_state[f"certificado_{alumno_id}"]
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE Alumnos SET certificado = %s WHERE alumno_id = %s", (nuevo_certificado, int(alumno_id)))
            conn.commit()
        st.success(f"Certificado del alumno {alumno_id} actualizado a {nuevo_certificado}.")
        st.rerun()
    except Exception as e:
        st.error(f"Error al actualizar certificado: {e}")
        conn.rollback()

def open_modal(modal_type, record_id):
    st.session_state.modal_tipo = modal_type
    st.session_state.modal_id = record_id

def close_modal_and_rerun():
    st.session_state.modal_tipo = None
    st.session_state.modal_id = None
    st.rerun()

# --- TABS PRINCIPALES ---
tab_alumnos, tab_grupos, tab_profesores = st.tabs([" Alumnos", " Grupos", " Profesores"])
conn = get_connection()

# --- PESTAÑA DE ALUMNOS ---
with tab_alumnos:
    st.header("Gestionar Alumnos")

    with st.expander(" Registrar Nuevo Alumno"):
        with st.form("nuevo_alumno_form", clear_on_submit=True):
            st.subheader("Datos del Nuevo Alumno")
            df_grupos_options = pd.read_sql("SELECT grupo_id, nombre_grupo FROM Grupos WHERE status_grupo = 'Activo' ORDER BY nombre_grupo ASC", conn)

            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre completo")
                matricula = st.text_input("Matrícula")
                correo = st.text_input("Correo electrónico")
                fecha_nacimiento = st.date_input("Fecha de Nacimiento", value=None, min_value=datetime.date(1950, 1, 1), max_value=datetime.date.today())
            with col2:
                telefono = st.text_input("Teléfono")
                estado = st.text_input("Estado de residencia")
                if not df_grupos_options.empty:
                    grupo_seleccionado_id = st.selectbox("Asignar al Grupo", options=df_grupos_options['grupo_id'], format_func=lambda x: df_grupos_options.loc[df_grupos_options['grupo_id'] == x, 'nombre_grupo'].iloc[0], index=None, placeholder="Selecciona un grupo...")
                else:
                    st.warning("No hay grupos 'Activos' disponibles.")
                    grupo_seleccionado_id = None
            
            # Botón Azul Sólido
            submitted = st.form_submit_button("Registrar Alumno", type="primary")
            
            if submitted: 
                if not all([nombre, matricula, correo, fecha_nacimiento, telefono, estado, grupo_seleccionado_id]):
                    st.error("🚨 ¡Error! Todos los campos son obligatorios para el registro.")
                else:
                    try:
                        with conn.cursor() as cur:
                            sql_alumno = "INSERT INTO Alumnos (nombre_completo, status_alumno, matricula, correo, telefono, estado_residencia, fecha_nacimiento, certificado) VALUES (%s, 'Activo', %s, %s, %s, %s, %s, 'Pendiente') RETURNING alumno_id"
                            cur.execute(sql_alumno, (nombre, matricula, correo, telefono, estado, fecha_nacimiento))
                            new_alumno_id = cur.fetchone()[0]
                            sql_inscripcion = "INSERT INTO Inscripciones (alumno_id, grupo_id) VALUES (%s, %s)"
                            cur.execute(sql_inscripcion, (new_alumno_id, int(grupo_seleccionado_id)))
                            conn.commit()
                        st.success("¡Alumno registrado e inscrito con éxito!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al registrar alumno: {e}")
                        conn.rollback()

    
    # (CORREGIDO): Se usa st.container(border=True) para agrupar filtros Y tabla
    with st.container(border=True):
        st.subheader("Lista de Alumnos")

        col_filter1, col_filter2, col_filter3 = st.columns([1, 1, 2])
        with col_filter1:
            df_grupos_filtro = pd.read_sql("SELECT grupo_id, nombre_grupo FROM Grupos ORDER BY nombre_grupo ASC", conn)
            opciones_filtro = {0: "Mostrar Todos los Grupos"}
            opciones_filtro.update(pd.Series(df_grupos_filtro.nombre_grupo.values, index=df_grupos_filtro.grupo_id).to_dict())
            grupo_id_seleccionado = st.selectbox("Filtrar por Grupo", options=list(opciones_filtro.keys()), format_func=lambda x: opciones_filtro[x])
        
        with col_filter2:
            status_options = ["Todos", "Activo", "Restringido", "Baja"]
            status_filter = st.selectbox("Filtrar por Status", options=status_options, index=0)

        with col_filter3:
            st.write("") # Add vertical spacing to align with filters
            col_search_button, col_search_input = st.columns([0.15, 0.85]) # Button first
            with col_search_button:
                if st.button("🔍", key="search_alumnos_button", use_container_width=True):
                    st.session_state["search_value_alumnos"] = st.session_state["search_alumnos_realtime"]
            with col_search_input:
                search_term = st.text_input(
                    "Buscar Alumno",
                    placeholder="Buscar por nombre, matrícula o correo...",
                    key="search_alumnos_realtime",
                    value=st.session_state.get("search_value_alumnos", ""),
                    label_visibility="collapsed" # Ocultar la etiqueta
                )
        


    try:
        query_alumnos = "SELECT a.*, g.nombre_grupo FROM Alumnos a LEFT JOIN Inscripciones i ON a.alumno_id = i.alumno_id LEFT JOIN Grupos g ON i.grupo_id = g.grupo_id"
        params = []
        where_clauses = []

        if grupo_id_seleccionado != 0:
            where_clauses.append("g.grupo_id = %s")
            params.append(grupo_id_seleccionado)
        
        if status_filter == "Todos":
            where_clauses.append("a.status_alumno IN ('Activo', 'Restringido', 'Baja')")
            where_clauses.append("g.grupo_id IS NOT NULL")
        elif status_filter == "Activo":
            where_clauses.append("a.status_alumno = 'Activo'")
            where_clauses.append("g.grupo_id IS NOT NULL")
        elif status_filter in ("Restringido", "Baja"):
            where_clauses.append("a.status_alumno = %s")
            params.append(status_filter)
        else:
            where_clauses.append("a.status_alumno != 'Finalizado'")

        if where_clauses:
            query_alumnos += " WHERE " + " AND ".join(where_clauses)
        
        query_alumnos += " ORDER BY g.nombre_grupo ASC, a.nombre_completo ASC;"
        df_alumnos_raw = pd.read_sql(query_alumnos, conn, params=tuple(params))

        if search_term and search_term.strip():
            search_term_clean = search_term.strip()
            df_alumnos_raw = df_alumnos_raw[
                df_alumnos_raw["nombre_completo"].str.contains(search_term_clean, case=False, na=False) | 
                df_alumnos_raw["matricula"].str.contains(search_term_clean, case=False, na=False) | 
                df_alumnos_raw["correo"].str.contains(search_term_clean, case=False, na=False)
            ]
        
        if df_alumnos_raw.empty:
            st.info("No se encontraron alumnos con los filtros seleccionados.")
        else:
            
            # (CORREGIDO): Función para renderizar el botón de editar (Amarillo)
            def render_acciones_alumno(row):
                st.markdown('<div class="btn-warning">', unsafe_allow_html=True)
                st.button("✏️ Editar", key=f"edit_alumno_{row['alumno_id']}", on_click=open_modal, args=("edit_alumno", row['alumno_id']), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            grupos_en_data = df_alumnos_raw['nombre_grupo'].fillna("Alumnos sin grupo").unique()
            for grupo in grupos_en_data:
                st.markdown(f"<h4 style='text-align: left; color: #3498DB; margin-top: 20px;'>Grupo: {grupo}</h4>", unsafe_allow_html=True)
                df_grupo_actual = df_alumnos_raw[df_alumnos_raw['nombre_grupo'].fillna("Alumnos sin grupo") == grupo]
                renderers = {
                    "Acciones": render_acciones_alumno, # <-- Botón Amarillo
                    "Nombre": lambda row: st.write(row['nombre_completo']),
                    "Grupo": lambda row: st.write(row['nombre_grupo']),
                    "Status": lambda row: st.selectbox("Status", ["Activo", "Baja", "Restringido", "Finalizado"], index=["Activo", "Baja", "Restringido", "Finalizado"].index(row['status_alumno']), key=f"status_{row['alumno_id']}", on_change=handle_status_change, args=(row['alumno_id'],), label_visibility="collapsed"),
                    "Certificado": lambda row: st.selectbox("Certificado", ["Pendiente", "Certificado"], index=["Pendiente", "Certificado"].index(row['certificado']), key=f"certificado_{row['alumno_id']}", on_change=handle_certificado_change, args=(row['alumno_id'],), label_visibility="collapsed"),
                    "Matrícula": lambda row: st.write(row['matricula']),
                    "Correo": lambda row: st.write(row['correo']),
                    "Teléfono": lambda row: st.write(row['telefono']),
                    "Fecha Nacimiento": lambda row: st.write(row['fecha_nacimiento'].strftime('%d/%m/%Y') if pd.notna(row['fecha_nacimiento']) else "N/A"),
                }
                st.markdown('<div class="table-container">', unsafe_allow_html=True)
                display_data_table(
                    df=df_grupo_actual,
                    col_widths=[3, 4, 1.5, 4, 4, 3, 4, 3, 3],
                    headers=["Acciones", "Nombre", "Grupo", "Status", "Certificado", "Matrícula", "Correo", "Teléfono", "Fecha Nacimiento"],
                    custom_renderers=renderers
                )
                st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error al cargar la lista de alumnos: {e}")

    # (CORREGIDO): Cierre de la tarjeta flotante
    st.markdown('</div>', unsafe_allow_html=True)

# --- PESTAÑA DE GRUPOS ---
with tab_grupos:
    st.header("Gestionar Grupos")
    
    # --- LÓGICA DE ACTUALIZACIÓN AUTOMÁTICA DE STATUS ---
    try:
        today = datetime.date.today()
        with conn.cursor() as cur:
            # 1. (EXISTENTE) Activa grupos 'Próximos' cuya fecha de inicio ya llegó
            cur.execute("UPDATE Grupos SET status_grupo = 'Activo' WHERE status_grupo = 'Próximo' AND fecha_inicio <= %s", (today,))
            
            # 2. (NUEVO) Finaliza grupos 'Activos' cuya fecha de término ya pasó
            cur.execute("UPDATE Grupos SET status_grupo = 'Finalizado' WHERE status_grupo = 'Activo' AND fecha_termino < %s", (today,))
            
            conn.commit()
    except Exception as e:
        st.warning(f"No se pudo ejecutar la actualización automática de status: {e}")
        conn.rollback()
    
    # --- FORMULARIO DE AÑADIR NUEVO GRUPO ---
    with st.expander("Añadir Nuevo Grupo"):
        with st.form("nuevo_grupo_form", clear_on_submit=True):
            st.subheader("Datos del Nuevo Grupo")
            df_profesores_options = pd.read_sql("SELECT profesor_id, nombre_completo FROM Profesores WHERE status = 'Activo' ORDER BY nombre_completo ASC", conn)
            
            col1, col2 = st.columns(2)
            with col1:
                nombre_grupo = st.text_input("Nombre del Grupo")
                
                # (CAMBIO) 'status_grupo' inicia vacío
                status_grupo = st.selectbox(
                    "Status del Grupo", 
                    ["Activo", "Próximo"], 
                    index=None, 
                    placeholder="Selecciona un status..."
                )
                
                if not df_profesores_options.empty:
                    # (CAMBIO) 'profesor_id' inicia vacío
                    profesor_id = st.selectbox(
                        "Asignar Profesor", 
                        options=df_profesores_options['profesor_id'], 
                        format_func=lambda x: df_profesores_options.loc[df_profesores_options['profesor_id'] == x, 'nombre_completo'].iloc[0],
                        index=None,
                        placeholder="Selecciona un profesor..."
                    )
                else:
                    st.warning("No hay profesores 'Activos' disponibles.")
                    profesor_id = None
            
            with col2:
                # (CAMBIO) 'fecha_inicio' por defecto hoy
                fecha_inicio = st.date_input("Fecha de Inicio", value=datetime.date.today())
                
                # (CAMBIO) 'fecha_termino' inicia vacía
                fecha_termino = st.date_input("Fecha de Término", value=None)
            
            # Botón Azul Sólido
            submitted_grupo = st.form_submit_button("Añadir Grupo", type="primary")

            if submitted_grupo:
                # (NUEVO) Validación robusta para todos los campos
                valid = True
                if not all([nombre_grupo, status_grupo, profesor_id, fecha_inicio, fecha_termino]):
                    st.error("🚨 ¡Error! Todos los campos son obligatorios.")
                    valid = False
                else:
                    today = datetime.date.today()
                    
                    # (NUEVO) Validación: Fecha de inicio no puede ser pasada
                    if fecha_inicio < today:
                        st.error("❌ Error: La Fecha de Inicio no puede ser anterior al día de hoy.")
                        valid = False
                    
                    # (EXISTENTE) Validación: Fecha de término vs inicio
                    if fecha_termino < fecha_inicio:
                        st.error("❌ Error: La Fecha de Término no puede ser anterior a la Fecha de Inicio.")
                        valid = False
                
                if valid:
                    try:
                        with conn.cursor() as cur:
                            sql = "INSERT INTO Grupos (nombre_grupo, status_grupo, profesor_id, fecha_inicio, fecha_termino) VALUES (%s, %s, %s, %s, %s)"
                            cur.execute(sql, (nombre_grupo, status_grupo, int(profesor_id), fecha_inicio, fecha_termino))
                            conn.commit()
                        st.success("Grupo añadido con éxito.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al añadir grupo: {e}")
                        conn.rollback()

    # --- LISTA DE GRUPOS (CON LA CORRECCIÓN DEL CONTENEDOR) ---
    with st.container(border=True):
        st.subheader("Lista de Grupos")
        
        try:
            query_grupos = "SELECT g.*, p.nombre_completo as nombre_profesor FROM Grupos g LEFT JOIN Profesores p ON g.profesor_id = p.profesor_id ORDER BY g.status_grupo ASC, g.nombre_grupo ASC"
            df_grupos = pd.read_sql(query_grupos, conn)
            
            col_search_button_grupos, col_search_input_grupos = st.columns([0.1, 0.9])
            with col_search_button_grupos:
                if st.button("🔍", key="search_grupos_button", use_container_width=True):
                    st.session_state["search_value_grupos"] = st.session_state["search_grupos_realtime"]
            with col_search_input_grupos:
                search_term_grupos = st.text_input(
                    "Buscar Grupo por nombre", 
                    key="search_grupos_realtime",
                    placeholder="Escribe para filtrar grupos...",
                    value=st.session_state.get("search_value_grupos", ""),
                    label_visibility="collapsed" # Ocultar la etiqueta
                )
            # st.session_state["search_value_grupos"] = search_term_grupos # Esta línea ya no es necesaria aquí

            if search_term_grupos and search_term_grupos.strip():
                df_grupos = df_grupos[df_grupos['nombre_grupo'].str.contains(search_term_grupos.strip(), case=False, na=False)]

            # (CORREGIDO): Función de renderizado con los colores solicitados
            def render_acciones_grupo(row):
                # Gracias a la lógica de auto-archivado, los grupos viejos
                # entrarán aquí automáticamente.
                if row['status_grupo'] == 'Finalizado':
                    # Botón Verde (Restablecer)
                    st.markdown('<div class="btn-success">', unsafe_allow_html=True)
                    st.button("♻️ Restablecer", key=f"reset_grupo_{row['grupo_id']}", on_click=open_modal, args=("reset_grupo", row['grupo_id']), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    # Grupos 'Activos' o 'Próximos'
                    col1, col2 = st.columns(2)
                    with col1:
                        # Botón Amarillo (Editar)
                        st.markdown('<div class="btn-warning">', unsafe_allow_html=True)
                        st.button("✏️ Editar", key=f"edit_grupo_{row['grupo_id']}", on_click=open_modal, args=("edit_grupo", row['grupo_id']), use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with col2:
                        # Botón Rojo (Finalizar)
                        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
                        st.button("✅ Finalizar", key=f"finalize_grupo_{row['grupo_id']}", on_click=open_modal, args=("finalize_grupo", row['grupo_id']), use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
            
            grupo_renderers = {
                "Acciones": render_acciones_grupo,
                "Grupo": lambda row: st.write(row['nombre_grupo']),
                "Status": lambda row: st.write(row['status_grupo']),
                "Fecha Inicio": lambda row: st.write(row['fecha_inicio'].strftime('%d/%m/%Y') if pd.notna(row['fecha_inicio']) else "N/A"),
                "Fecha Término": lambda row: st.write(row['fecha_termino'].strftime('%d/%m/%Y') if pd.notna(row['fecha_termino']) else "N/A"),
                "Profesor": lambda row: st.write(row['nombre_profesor'])
            }

            st.markdown('<div class="table-container">', unsafe_allow_html=True)
            display_data_table(
                df=df_grupos,
                col_widths=[3, 1.5, 1.5, 2, 2, 3],
                headers=["Acciones", "Grupo", "Status", "Fecha Inicio", "Fecha Término", "Profesor"],
                custom_renderers=grupo_renderers
            )
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error al cargar grupos: {e}")

# --- PESTAÑA DE PROFESORES ---
with tab_profesores:
    st.header("Gestionar Profesores")
    
    with st.expander(" Añadir Nuevo Profesor"):
        with st.form("nuevo_profesor_form", clear_on_submit=True):
            st.subheader("Datos del Nuevo Profesor")
            col1, col2 = st.columns(2)
            nombre_profesor = col1.text_input("Nombre Completo")
            status_profesor = col2.selectbox("Status del Profesor", ["Activo", "Inactivo"])
            
            # Botón Azul Sólido
            submitted_profesor = st.form_submit_button("Registrar Profesor", use_container_width=True, type="primary")

            if submitted_profesor: 
                if nombre_profesor:
                    try:
                        with conn.cursor() as cur:
                            cur.execute("INSERT INTO Profesores (nombre_completo, status) VALUES (%s, %s)", (nombre_profesor, status_profesor))
                            conn.commit()
                        st.success("Profesor registrado con éxito!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al registrar profesor: {e}")
                        conn.rollback()
                else:
                    st.warning("El nombre del profesor no puede estar vacío.")
    
    # (CORREGIDO): Tarjeta añadida para envolver búsqueda y tabla
    with st.container(border=True):
        st.subheader("Lista de Profesores")

        try:
            df_profesores = pd.read_sql("SELECT * FROM Profesores ORDER BY profesor_id ASC", conn)
            
            col_search_button_profesores, col_search_input_profesores = st.columns([0.05, 0.95])
            with col_search_button_profesores:
                if st.button("🔍", key="search_profesores_button", use_container_width=True):
                    st.session_state["search_value_profesores"] = st.session_state["search_profesores_realtime"]
            with col_search_input_profesores:
                search_profesores = st.text_input(
                "Buscar Profesor", 
                key="search_profesores_realtime",
                placeholder="Escribe para filtrar profesores...",
                value=st.session_state.get("search_value_profesores", ""),
                label_visibility="collapsed" # Ocultar la etiqueta
                )
            # st.session_state["search_value_profesores"] = search_profesores # Esta línea ya no es necesaria aquí
            
            
            if search_profesores and search_profesores.strip():
                df_profesores = df_profesores[df_profesores['nombre_completo'].str.contains(search_profesores.strip(), case=False, na=False)]

            # (CORREGIDO): Función de renderizado con los colores solicitados
            def render_acciones_profesor(row):
                col1, col2 = st.columns(2)
                with col1:
                    # Botón Amarillo (Editar)
                    st.markdown('<div class="btn-warning">', unsafe_allow_html=True)
                    st.button("✏️ Editar", key=f"edit_prof_{row['profesor_id']}", on_click=open_modal, args=("edit_profesor", row['profesor_id']), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                with col2:
                    # Botón Rojo (Baja)
                    st.markdown(f'<div class="btn-danger">', unsafe_allow_html=True)
                    st.button("❌ Baja", key=f"delete_prof_{row['profesor_id']}", on_click=open_modal, args=("delete_profesor", row['profesor_id']), use_container_width=True)
                    st.markdown(f'</div>', unsafe_allow_html=True)

            profesor_renderers = {
                "Acciones": render_acciones_profesor,
                "Nombre Completo": lambda row: st.write(row['nombre_completo']),
                "Status": lambda row: st.write(row['status'])
            }

            st.markdown('<div class="table-container">', unsafe_allow_html=True)
            display_data_table(df_profesores, [2, 3, 2], ["Acciones", "Nombre Completo", "Status"], profesor_renderers)
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error al cargar la lista de profesores: {e}")


# --- DEFINICIONES DE MODALES ---

@st.dialog("✏️ Editar Alumno")
def modal_editar_alumno(alumno_data, conn):
    # ... (código de carga de datos del modal) ...
    df_grupos_options = pd.read_sql("SELECT grupo_id, nombre_grupo FROM Grupos WHERE status_grupo = 'Activo' ORDER BY nombre_grupo ASC", conn)
    opciones_grupo = {0: "Sin Asignar"}
    opciones_grupo.update(pd.Series(df_grupos_options.nombre_grupo.values, index=df_grupos_options.grupo_id.astype(int)).to_dict())
    current_grupo_id = 0
    try:
        # Consulta mejorada para obtener el grupo más reciente del alumno
        query = f"""
        SELECT i.grupo_id 
        FROM Inscripciones i 
        WHERE i.alumno_id = {int(alumno_data['alumno_id'])}
        ORDER BY i.inscripcion_id DESC 
        LIMIT 1
        """
        result = pd.read_sql(query, conn)
        if not result.empty:
            current_grupo_id = int(result.iloc[0]['grupo_id'])
            # Verificar si el grupo existe en las opciones
            if current_grupo_id not in opciones_grupo:
                # Obtener el nombre del grupo aunque no esté activo
                grupo_query = f"SELECT nombre_grupo FROM Grupos WHERE grupo_id = {current_grupo_id}"
                grupo_result = pd.read_sql(grupo_query, conn)
                if not grupo_result.empty:
                    # Añadir el grupo a las opciones aunque no esté activo
                    opciones_grupo[current_grupo_id] = f"{grupo_result.iloc[0]['nombre_grupo']} (Inactivo)"
                    # Actualizar la lista de opciones
                    lista_ids_opciones = list(opciones_grupo.keys())
    except Exception as e:
        st.error(f"Error al obtener grupo: {e}")
        pass
    lista_ids_opciones = list(opciones_grupo.keys())
    current_index = lista_ids_opciones.index(current_grupo_id) if current_grupo_id in lista_ids_opciones else 0

    with st.form("edit_alumno_form"):
        st.subheader(f"Editando a: {alumno_data['nombre_completo']}")
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre", value=alumno_data["nombre_completo"])
            matricula = st.text_input("Matrícula", value=alumno_data["matricula"])
            correo = st.text_input("Correo", value=alumno_data["correo"])
            nuevo_grupo_id = st.selectbox("Asignar a Grupo", options=lista_ids_opciones, format_func=lambda x: opciones_grupo[x], index=current_index)
        with col2:
            telefono = st.text_input("Teléfono", value=alumno_data["telefono"])
            estado = st.text_input("Estado de residencia", value=alumno_data["estado_residencia"])
            status_list = ["Activo", "Baja", "Restringido", "Finalizado"]
            if alumno_data['status_alumno'] not in status_list: status_list.append(alumno_data['status_alumno'])
            current_status_index = status_list.index(alumno_data['status_alumno'])
            status = st.selectbox("Status", status_list, index=current_status_index)
            fecha_nacimiento = st.date_input("Fecha de Nacimiento", value=pd.to_datetime(alumno_data["fecha_nacimiento"]), min_value=datetime.date(1950, 1, 1), max_value=datetime.date(2025, 12, 31))

        c1, c2 = st.columns(2)
        
        # (CORREGIDO): Botón Verde (Actualizar)
        with c1:
            st.markdown('<div class="btn-success">', unsafe_allow_html=True)
            submitted = st.form_submit_button("Actualizar", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # (CORREGIDO): Botón Rojo (Cancelar)
        with c2:
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            cancelled = st.form_submit_button("Cancelar", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            # ... (lógica de actualización) ...
            alumno_id_int = int(alumno_data["alumno_id"])
            try:
                with conn.cursor() as cur:
                    sql_alumno = "UPDATE Alumnos SET nombre_completo=%s, status_alumno=%s, matricula=%s, correo=%s, telefono=%s, estado_residencia=%s, fecha_nacimiento=%s WHERE alumno_id=%s"
                    cur.execute(sql_alumno, (nombre, status, matricula, correo, telefono, estado, fecha_nacimiento, alumno_id_int))
                    
                    cur.execute("SELECT i.inscripcion_id FROM Inscripciones i WHERE i.alumno_id = %s AND EXISTS (SELECT 1 FROM Pagos p WHERE p.inscripcion_id = i.inscripcion_id)", (alumno_id_int,))
                    insc_con_pagos = cur.fetchone()
                    
                    if insc_con_pagos:
                        if nuevo_grupo_id != 0:
                            cur.execute("UPDATE Inscripciones SET grupo_id = %s WHERE alumno_id = %s", (int(nuevo_grupo_id), alumno_id_int))
                        else:
                            st.warning("Advertencia: El alumno fue desasignado de grupo, pero tenía pagos registrados.")
                    else:
                        cur.execute("DELETE FROM Inscripciones WHERE alumno_id = %s", (alumno_id_int,))
                        if nuevo_grupo_id != 0:
                            cur.execute("INSERT INTO Inscripciones (alumno_id, grupo_id) VALUES (%s, %s)", (alumno_id_int, int(nuevo_grupo_id)))
                    
                    conn.commit()
                    st.success("Alumno actualizado con éxito.")
                    close_modal_and_rerun()
            except Exception as e:
                st.error(f"Error al actualizar alumno: {e}")
                conn.rollback()
        
        if cancelled:
            close_modal_and_rerun()

@st.dialog("✏️ Editar Grupo")
def modal_editar_grupo(grupo_data, conn):
    # ... (código de carga de datos del modal) ...
    df_profesores_options = pd.read_sql("SELECT profesor_id, nombre_completo FROM Profesores WHERE status = 'Activo'", conn)
    with st.form("edit_grupo_form"):
        st.subheader(f"Editando Grupo: {grupo_data['nombre_grupo']}")
        nombre_grupo = st.text_input("Nombre del Grupo", value=grupo_data['nombre_grupo'])
        status_grupo = st.selectbox("Status", ["Activo", "Próximo"], index=["Activo", "Próximo"].index(grupo_data['status_grupo']) if grupo_data['status_grupo'] in ["Activo", "Próximo"] else 0)
        prof_index = df_profesores_options[df_profesores_options['profesor_id'] == grupo_data['profesor_id']].index
        prof_id_options = df_profesores_options['profesor_id']
        prof_id = st.selectbox("Profesor", options=prof_id_options, index=int(prof_index[0]) if len(prof_index) > 0 else 0, format_func=lambda x: df_profesores_options[df_profesores_options['profesor_id'] == x]['nombre_completo'].values[0])
        col1, col2 = st.columns(2)
        with col1: fecha_inicio = st.date_input("Fecha de Inicio", value=pd.to_datetime(grupo_data["fecha_inicio"]))
        with col2: fecha_termino = st.date_input("Fecha de Término", value=pd.to_datetime(grupo_data["fecha_termino"]))
        
        c1, c2 = st.columns(2)
        # (CORREGIDO): Botón Verde (Actualizar)
        with c1:
            st.markdown('<div class="btn-success">', unsafe_allow_html=True)
            submitted = c1.form_submit_button("Actualizar", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        # (CORREGIDO): Botón Rojo (Cancelar)
        with c2:
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            cancelled = c2.form_submit_button("Cancelar", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            # ... (lógica de actualización) ...
            valid = True; today = datetime.date.today()
            if fecha_termino < fecha_inicio: st.error("❌ Error: La Fecha de Término no puede ser anterior."); valid = False
            # ... (resto de validaciones) ...
            
            if valid:
                try:
                    with conn.cursor() as cur:
                        sql = "UPDATE Grupos SET nombre_grupo=%s, status_grupo=%s, profesor_id=%s, fecha_inicio=%s, fecha_termino=%s WHERE grupo_id=%s"
                        cur.execute(sql, (nombre_grupo, status_grupo, int(prof_id), fecha_inicio, fecha_termino, int(grupo_data['grupo_id'])))
                        conn.commit()
                    st.success("Grupo actualizado.")
                    close_modal_and_rerun()
                except Exception as e:
                    st.error(f"Error al actualizar el grupo: {e}")
                    conn.rollback()
        
        if cancelled:
            close_modal_and_rerun()

@st.dialog("✅ Finalizar y Archivar Grupo")
def modal_finalizar_grupo(grupo_id, conn):
    st.warning(f"¿Finalizar grupo ID {grupo_id}? Se guardará historial, alumnos 'Activos' pasarán a 'Finalizado' y se desvincularán.")
    col1, col2 = st.columns(2)
    
    # (CORREGIDO): Botón Rojo (Confirmar)
    with col1:
        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
        confirm_clicked = st.button("Confirmar Finalización", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # (CORREGIDO): Botón Gris (Cancelar - Más seguro para UX)
    with col2:
        cancel_clicked = st.button("Cancelar", use_container_width=True, type="secondary")

    if confirm_clicked:
        try:
            # ... (lógica de finalización) ...
            with conn.cursor() as cur:
                grupo_id_int = int(grupo_id)
                cur.execute("UPDATE Alumnos a SET status_alumno = 'Finalizado' FROM Inscripciones i WHERE a.alumno_id = i.alumno_id AND i.grupo_id = %s AND a.status_alumno = 'Activo';", (grupo_id_int,))
                cur.execute("SELECT g.nombre_grupo, p.nombre_completo, g.fecha_inicio, g.fecha_termino FROM Grupos g JOIN Profesores p ON g.profesor_id = p.profesor_id WHERE g.grupo_id = %s", (grupo_id_int,))
                grupo_info = cur.fetchone()
                if grupo_info:
                    nombre_grupo, nombre_profesor, fecha_inicio, fecha_termino = grupo_info
                    df_alumnos_grupo = pd.read_sql("SELECT a.nombre_completo, a.matricula, a.status_alumno, a.certificado FROM Alumnos a JOIN Inscripciones i ON a.alumno_id = i.alumno_id WHERE i.grupo_id = %s", conn, params=(grupo_id_int,))
                    alumnos_list_final = [{'nombre': al['nombre_completo'], 'matricula': al['matricula'], 'status_final': al['status_alumno'], 'certificado': al['certificado']} for i, al in df_alumnos_grupo.iterrows()]
                    snapshot_json = json.dumps({"alumnos": alumnos_list_final}, indent=4, default=str)
                    cur.execute("INSERT INTO Grupos_Historial (nombre_grupo, nombre_profesor, datos_grupo_alumnos, fecha_inicio, fecha_termino) VALUES (%s, %s, %s, %s, %s)", (nombre_grupo, nombre_profesor, snapshot_json, fecha_inicio, fecha_termino))
                    cur.execute("DELETE FROM Inscripciones WHERE grupo_id = %s", (grupo_id_int,))
                    cur.execute("UPDATE Grupos SET status_grupo = 'Finalizado' WHERE grupo_id = %s", (grupo_id_int,))
                    conn.commit()
                    st.success("Grupo finalizado y archivado.")
                else: st.error("No se encontró el grupo.")
            close_modal_and_rerun()
        except Exception as e:
            st.error(f"Error al finalizar grupo: {e}")
            conn.rollback()
            
    if cancel_clicked:
        close_modal_and_rerun()

@st.dialog("♻️ Restablecer Grupo")
def modal_restablecer_grupo(grupo_id, conn):
    df_profesores_options = pd.read_sql("SELECT profesor_id, nombre_completo FROM Profesores WHERE status = 'Activo'", conn)
    with st.form("reset_grupo_form"):
        st.info(f"Reactivar grupo ID {grupo_id}. Asigna profesor y fechas.")
        profesor_id = st.selectbox("Asignar Nuevo Profesor", options=df_profesores_options['profesor_id'], format_func=lambda x: df_profesores_options.loc[df_profesores_options['profesor_id'] == x, 'nombre_completo'].iloc[0])
        nueva_fecha_inicio = st.date_input("Nueva Fecha de Inicio", value=datetime.date.today())
        nueva_fecha_termino = st.date_input("Nueva Fecha de Término", value=datetime.date.today() + datetime.timedelta(days=30))
        
        c1, c2 = st.columns(2)
        # (CORREGIDO): Botón Verde (Restablecer)
        with c1:
            st.markdown('<div class="btn-success">', unsafe_allow_html=True)
            submitted = c1.form_submit_button("Confirmar y Restablecer", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        # (CORREGIDO): Botón Rojo (Cancelar)
        with c2:
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            cancelled = c2.form_submit_button("Cancelar", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            try:
                with conn.cursor() as cur:
                    sql = "UPDATE Grupos SET status_grupo = 'Activo', profesor_id = %s, fecha_inicio = %s, fecha_termino = %s WHERE grupo_id = %s"
                    cur.execute(sql, (int(profesor_id), nueva_fecha_inicio, nueva_fecha_termino, int(grupo_id)))
                    conn.commit()
                st.success("Grupo restablecido.")
                close_modal_and_rerun()
            except Exception as e:
                st.error(f"Error al restablecer: {e}")
                conn.rollback()
        
        if cancelled:
            close_modal_and_rerun()

@st.dialog("✏️ Editar Profesor")
def modal_editar_profesor(profesor_data, conn):
    with st.form("edit_profesor_form"):
        st.subheader(f"Editando a: {profesor_data['nombre_completo']}")
        nombre_profesor = st.text_input("Nombre Completo", value=profesor_data['nombre_completo'])
        st.write("")
        status_profesor = st.selectbox("Status", ["Activo", "Inactivo"], index=["Activo", "Inactivo"].index(profesor_data['status']))
        st.write("")
        
        c1, c2 = st.columns(2)
        # (CORREGIDO): Botón Verde (Actualizar)
        with c1:
            st.markdown('<div class="btn-success">', unsafe_allow_html=True)
            submitted = c1.form_submit_button("Actualizar", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        # (CORREGIDO): Botón Rojo (Cancelar)
        with c2:
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            cancelled = c2.form_submit_button("Cancelar", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            try:
                with conn.cursor() as cur:
                    sql = "UPDATE Profesores SET nombre_completo=%s, status=%s WHERE profesor_id=%s"
                    cur.execute(sql, (nombre_profesor, status_profesor, int(profesor_data['profesor_id'])))
                    conn.commit()
                st.success("Profesor actualizado.")
                close_modal_and_rerun()
            except Exception as e:
                st.error(f"Error al actualizar: {e}")
                conn.rollback()
        
        if cancelled:
            close_modal_and_rerun()

@st.dialog("❌ Dar de Baja Profesor")
def modal_eliminar_profesor(profesor_id, conn):
    st.warning(f"¿Dar de baja (marcar como 'Inactivo') al profesor ID {profesor_id}?")
    col1, col2 = st.columns(2)
    
    # (CORREGIDO): Botón Rojo (Confirmar)
    with col1:
        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
        confirm_baja = st.button("Confirmar Baja", key=f"delete_prof_{profesor_id}_confirm", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # (CORREGIDO): Botón Gris (Cancelar - Más seguro para UX)
    with col2:
        cancel_baja = st.button("Cancelar", use_container_width=True, type="secondary")

    if confirm_baja:
        try:
            with conn.cursor() as cur:
                cur.execute("UPDATE Profesores SET status='Inactivo' WHERE profesor_id=%s", (int(profesor_id),))
                conn.commit()
            st.success("Profesor dado de baja.")
            close_modal_and_rerun()
        except Exception as e:
            st.error(f"Error al dar de baja: {e}")
            conn.rollback()
            
    if cancel_baja:
        close_modal_and_rerun()

# --- LÓGICA PRINCIPAL PARA INVOCAR MODALES ---
if "modal_tipo" in st.session_state and st.session_state.modal_tipo is not None:
    tipo = st.session_state.modal_tipo
    obj_id = st.session_state.modal_id
    conn = get_connection()
    st.session_state.modal_tipo = None
    st.session_state.modal_id = None
    try:
        if tipo == "edit_alumno":
            alumno_data = pd.read_sql(f"SELECT * FROM Alumnos WHERE alumno_id = {obj_id}", conn).iloc[0]
            modal_editar_alumno(alumno_data, conn)
        elif tipo == "edit_grupo":
            grupo_data = pd.read_sql(f"SELECT * FROM Grupos WHERE grupo_id = {obj_id}", conn).iloc[0]
            modal_editar_grupo(grupo_data, conn)
        elif tipo == "finalize_grupo":
            modal_finalizar_grupo(obj_id, conn)
        elif tipo == "reset_grupo":
            modal_restablecer_grupo(obj_id, conn)
        elif tipo == "edit_profesor":
            profesor_data = pd.read_sql(f"SELECT * FROM Profesores WHERE profesor_id = {obj_id}", conn).iloc[0]
            modal_editar_profesor(profesor_data, conn)
        elif tipo == "delete_profesor":
            modal_eliminar_profesor(obj_id, conn)
    except IndexError:
        st.error("Error: No se encontró el registro. Refrescando...")
        st.rerun()
    except Exception as e:
        st.error(f"Error al procesar el modal: {e}")