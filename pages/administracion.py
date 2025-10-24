import streamlit as st
import psycopg2
import pandas as pd
import datetime
import json

# Asumiendo que tienes utils.css, si no, puedes comentar estas líneas
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
load_css()

# Header principal
st.markdown("""
<div class="main-header">
    <h1> Administración del Sistema</h1>
    <p>Gestiona alumnos, grupos y profesores de manera eficiente</p>
</div>
""", unsafe_allow_html=True)

# --- CONEXIÓN A LA BD ---

@st.cache_resource
def init_connection():
    return psycopg2.connect(st.secrets["DB_CONNECTION_STRING"])

def get_connection():
    conn = init_connection()
    try:
        conn.cursor().execute("SELECT 1")
    except (psycopg2.InterfaceError, psycopg2.OperationalError):
        st.cache_resource.clear()
        conn = init_connection()
    return conn

# --- FUNCIONES DE TABLA REFACTORIZADAS ---

def display_data_table(df, col_widths, headers, custom_renderers):
    """ Función genérica para mostrar una tabla de datos con columnas personalizadas. """
    header_cols = st.columns(col_widths)
    for i, header in enumerate(headers):
        header_cols[i].markdown(f"**{header}**")
    st.markdown("<hr style='margin-top:0;margin-bottom:0.5rem'>", unsafe_allow_html=True)

    for index, row in df.iterrows():
        row_cols = st.columns(col_widths)
        for i, header in enumerate(headers):
            renderer_func = custom_renderers.get(header)
            with row_cols[i]:
                if renderer_func:
                    renderer_func(row)
                else:
                    col_name = header.lower().replace(" ", "_")
                    if col_name in row and pd.notna(row[col_name]):
                        st.write(str(row[col_name]))

# --- HANDLERS Y FUNCIONES DE MODAL ---

def handle_status_change(alumno_id):
    nuevo_status = st.session_state[f"status_{alumno_id}"]
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("UPDATE Alumnos SET status_alumno = %s WHERE alumno_id = %s", (nuevo_status, int(alumno_id)))
        conn.commit()
    st.success(f"Status del alumno {alumno_id} actualizado a {nuevo_status}.")
    st.rerun()

def handle_certificado_change(alumno_id):
    nuevo_certificado = st.session_state[f"certificado_{alumno_id}"]
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("UPDATE Alumnos SET certificado = %s WHERE alumno_id = %s", (nuevo_certificado, int(alumno_id)))
        conn.commit()
    st.success(f"Certificado del alumno {alumno_id} actualizado a {nuevo_certificado}.")
    st.rerun()

def open_modal(modal_type, record_id):
    # Esta función SÓLO pone el estado. El rerun automático de Streamlit hace el resto.
    st.session_state.modal_tipo = modal_type
    st.session_state.modal_id = record_id

def close_modal_and_rerun():
    # Esta función se llama DESDE DENTRO de un modal para cerrarlo y refrescar
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

            if st.form_submit_button("Registrar Alumno"):
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

    st.subheader("Lista de Alumnos")
    
    col_filter1, col_filter2, col_filter3 = st.columns([1, 1, 2])
    with col_filter1:
        df_grupos_filtro = pd.read_sql("SELECT grupo_id, nombre_grupo FROM Grupos ORDER BY nombre_grupo ASC", conn)
        opciones_filtro = {0: "Mostrar Todos los Grupos"}
        opciones_filtro.update(pd.Series(df_grupos_filtro.nombre_grupo.values, index=df_grupos_filtro.grupo_id).to_dict())
        grupo_id_seleccionado = st.selectbox("Filtrar por Grupo", options=list(opciones_filtro.keys()), format_func=lambda x: opciones_filtro[x])
    
    with col_filter2:
        # --- CAMBIO AQUÍ ---
        # Volvemos a los nombres originales
        status_options = ["Todos", "Activo", "Restringido", "Baja"]
        # El default es "Todos" (index=0)
        status_filter = st.selectbox("Filtrar por Status", options=status_options, index=0)

    with col_filter3:
        search_term = st.text_input("Buscar Alumno", placeholder="🔍 Buscar por nombre, matrícula o correo...")

    try:
        # --- CAMBIO AQUÍ ---
        # Lógica de consulta modificada para las nuevas reglas de filtro
        
        query_alumnos = "SELECT a.*, g.nombre_grupo FROM Alumnos a LEFT JOIN Inscripciones i ON a.alumno_id = i.alumno_id LEFT JOIN Grupos g ON i.grupo_id = g.grupo_id"
        params = []
        where_clauses = []

        # 1. Filtro de Grupo (no cambia)
        if grupo_id_seleccionado != 0:
            where_clauses.append("g.grupo_id = %s")
            params.append(grupo_id_seleccionado)
        
        # 2. Lógica del Filtro de Status
        if status_filter == "Todos":
            # Muestra todos (menos Finalizado) PERO solo con grupo
            where_clauses.append("a.status_alumno IN ('Activo', 'Restringido', 'Baja')")
            where_clauses.append("g.grupo_id IS NOT NULL") # Excepción
        
        elif status_filter == "Activo":
            # Muestra solo Activos PERO solo con grupo
            where_clauses.append("a.status_alumno = 'Activo'")
            where_clauses.append("g.grupo_id IS NOT NULL") # Excepción

        elif status_filter in ("Restringido", "Baja"):
            # Estos filtros SÍ deben mostrar alumnos "sin grupo" para reactivarlos
            where_clauses.append("a.status_alumno = %s")
            params.append(status_filter)
        
        # Construir la consulta final
        if where_clauses:
            query_alumnos += " WHERE " + " AND ".join(where_clauses)
        else:
            # Si no hay filtros, por defecto no mostramos finalizados
             where_clauses.append("WHERE a.status_alumno != 'Finalizado'")
            
        query_alumnos += " ORDER BY g.nombre_grupo ASC, a.nombre_completo ASC;"
        df_alumnos_raw = pd.read_sql(query_alumnos, conn, params=tuple(params))

        # El resto del código de búsqueda y renderizado no cambia
        if search_term:
            df_alumnos_raw = df_alumnos_raw[
                df_alumnos_raw["nombre_completo"].str.contains(search_term, case=False, na=False) | 
                df_alumnos_raw["matricula"].str.contains(search_term, case=False, na=False) | 
                df_alumnos_raw["correo"].str.contains(search_term, case=False, na=False)
            ]
        
        if df_alumnos_raw.empty:
            st.info("No se encontraron alumnos con los filtros seleccionados.")
        else:
            # (El resto del código para mostrar la tabla no cambia)
            grupos_en_data = df_alumnos_raw['nombre_grupo'].fillna("Alumnos sin grupo").unique()
            for grupo in grupos_en_data:
                st.markdown(f"<h4 style='text-align: left; color: #3498DB; margin-top: 20px;'>Grupo: {grupo}</h4>", unsafe_allow_html=True)
                df_grupo_actual = df_alumnos_raw[df_alumnos_raw['nombre_grupo'].fillna("Alumnos sin grupo") == grupo]
                renderers = {
                    "Acciones": lambda row: st.button("✏️ Editar", key=f"edit_alumno_{row['alumno_id']}", on_click=open_modal, args=("edit_alumno", row['alumno_id']), use_container_width=True),
                    "Nombre": lambda row: st.write(row['nombre_completo']),
                    "Grupo": lambda row: st.write(row['nombre_grupo']),
                    "Status": lambda row: st.selectbox("Status", ["Activo", "Baja", "Restringido", "Finalizado"], index=["Activo", "Baja", "Restringido", "Finalizado"].index(row['status_alumno']), key=f"status_{row['alumno_id']}", on_change=handle_status_change, args=(row['alumno_id'],), label_visibility="collapsed"),
                    "Certificado": lambda row: st.selectbox("Certificado", ["Pendiente", "Certificado"], index=["Pendiente", "Certificado"].index(row['certificado']), key=f"certificado_{row['alumno_id']}", on_change=handle_certificado_change, args=(row['alumno_id'],), label_visibility="collapsed"),
                    "Matrícula": lambda row: st.write(row['matricula']),
                    "Correo": lambda row: st.write(row['correo']),
                    "Teléfono": lambda row: st.write(row['telefono']),
                    "Fecha Nacimiento": lambda row: st.write(row['fecha_nacimiento'].strftime('%d/%m/%Y') if pd.notna(row['fecha_nacimiento']) else "N/A"),
                }
                display_data_table(
                    df=df_grupo_actual,
                    col_widths=[1.5, 3, 2, 2, 2, 2, 3, 2, 2],
                    headers=["Acciones", "Nombre", "Grupo", "Status", "Certificado", "Matrícula", "Correo", "Teléfono", "Fecha Nacimiento"],
                    custom_renderers=renderers
                )
    except Exception as e:
        st.error(f"Error al cargar la lista de alumnos: {e}")

# --- PESTAÑA DE GRUPOS ---
with tab_grupos:
    st.header("Gestionar Grupos")
    
    # --- ¡NUEVA LÓGICA! (Punto 1: Auto-actualización) ---
    try:
        today = datetime.date.today()
        with conn.cursor() as cur:
            # Esta consulta "promueve" grupos cuya fecha de inicio ha llegado
            cur.execute("""
                UPDATE Grupos 
                SET status_grupo = 'Activo' 
                WHERE status_grupo = 'Próximo' AND fecha_inicio <= %s
            """, (today,))
            conn.commit()
    except Exception as e:
        st.warning(f"No se pudo ejecutar la actualización automática de status: {e}")
    # --- Fin de la nueva lógica ---

    
    # --- (Punto 2) Formulario "Añadir Nuevo Grupo" modificado ---
    with st.expander("Añadir Nuevo Grupo"):
        with st.form("nuevo_grupo_form", clear_on_submit=True):
            st.subheader("Datos del Nuevo Grupo")
            df_profesores_options = pd.read_sql("SELECT profesor_id, nombre_completo FROM Profesores WHERE status = 'Activo' ORDER BY nombre_completo ASC", conn)
            
            col1, col2 = st.columns(2)
            with col1:
                nombre_grupo = st.text_input("Nombre del Grupo")
                st.write("") # Espacio
                
                # 'Finalizado' ha sido removido
                status_grupo = st.selectbox("Status del Grupo", ["Activo", "Próximo"])
                st.write("") # Espacio

                if not df_profesores_options.empty:
                    profesor_id = st.selectbox("Asignar Profesor", options=df_profesores_options['profesor_id'], format_func=lambda x: df_profesores_options.loc[df_profesores_options['profesor_id'] == x, 'nombre_completo'].iloc[0])
                else:
                    st.warning("No hay profesores 'Activos'.")
                    profesor_id = None
            
            with col2:
                fecha_inicio = st.date_input("Fecha de Inicio", value=datetime.date.today())
                st.write("") # Espacio
                fecha_termino = st.date_input("Fecha de Término", value=datetime.date.today() + datetime.timedelta(days=30))
            
            st.write("") # Espacio
            if st.form_submit_button("Añadir Grupo") and profesor_id and nombre_grupo:
                
                # --- ¡NUEVA LÓGICA! (Validaciones) ---
                today = datetime.date.today()
                valid = True
                
                # Regla 1: Término >= Inicio
                if fecha_termino < fecha_inicio:
                    st.error("Error: La Fecha de Término no puede ser anterior a la Fecha de Inicio.")
                    valid = False
                
                # Regla 2: 'Próximo' debe ser en el futuro
                if status_grupo == "Próximo" and fecha_inicio <= today:
                    st.error("Error: Un grupo 'Próximo' debe tener una Fecha de Inicio futura (después de hoy).")
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

    # (El resto de tu código de "Lista de Grupos" no cambia)
    st.subheader("Lista de Grupos")
    try:
        query_grupos = "SELECT g.*, p.nombre_completo as nombre_profesor FROM Grupos g LEFT JOIN Profesores p ON g.profesor_id = p.profesor_id ORDER BY g.status_grupo ASC, g.nombre_grupo ASC"
        df_grupos = pd.read_sql(query_grupos, conn)
        
        search_term_grupos = st.text_input("🔍 Buscar Grupo por nombre", key="search_grupos")
        if search_term_grupos:
            df_grupos = df_grupos[df_grupos['nombre_grupo'].str.contains(search_term_grupos, case=False, na=False)]

        def render_acciones_grupo(row):
            if row['status_grupo'] == 'Finalizado':
                st.button("♻️ Restablecer", key=f"reset_grupo_{row['grupo_id']}", on_click=open_modal, args=("reset_grupo", row['grupo_id']), use_container_width=True)
            else:
                col1, col2 = st.columns(2)
                col1.button("✏️ Editar", key=f"edit_grupo_{row['grupo_id']}", on_click=open_modal, args=("edit_grupo", row['grupo_id']), use_container_width=True)
                col2.button("✅ Finalizar", key=f"finalize_grupo_{row['grupo_id']}", on_click=open_modal, args=("finalize_grupo", row['grupo_id']), use_container_width=True)
        
        grupo_renderers = {
            "Acciones": render_acciones_grupo,
            "Grupo": lambda row: st.write(row['nombre_grupo']),
            "Status": lambda row: st.write(row['status_grupo']),
            "Fecha Inicio": lambda row: st.write(row['fecha_inicio'].strftime('%d/%m/%Y') if pd.notna(row['fecha_inicio']) else "N/A"),
            "Fecha Término": lambda row: st.write(row['fecha_termino'].strftime('%d/%m/%Y') if pd.notna(row['fecha_termino']) else "N/A"),
            "Profesor": lambda row: st.write(row['nombre_profesor'])
        }

        display_data_table(
            df=df_grupos,
            col_widths=[4, 2, 1.5, 2, 2, 3],
            headers=["Acciones", "Grupo", "Status", "Fecha Inicio", "Fecha Término", "Profesor"],
            custom_renderers=grupo_renderers
        )
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
            
            if st.form_submit_button("Registrar Profesor", use_container_width=True):
                if nombre_profesor:
                    try:
                        with conn.cursor() as cur:
                            cur.execute("INSERT INTO Profesores (nombre_completo, status) VALUES (%s, %s)", (nombre_profesor, status_profesor))
                            conn.commit()
                        st.success("Profesor registrado con éxito!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al registrar profesor: {e}")
                else:
                    st.warning("El nombre del profesor no puede estar vacío.")
    
    st.subheader("Lista de Profesores")
    try:
        df_profesores = pd.read_sql("SELECT * FROM Profesores ORDER BY profesor_id ASC", conn)
        
        search_profesores = st.text_input("🔍 Buscar Profesor", key="search_profesores")
        if search_profesores:
            df_profesores = df_profesores[df_profesores['nombre_completo'].str.contains(search_profesores, case=False, na=False)]

        def render_acciones_profesor(row):
            col1, col2 = st.columns(2)
            col1.button("✏️ Editar", key=f"edit_prof_{row['profesor_id']}", on_click=open_modal, args=("edit_profesor", row['profesor_id']), use_container_width=True)
            col2.button("❌ Baja", key=f"delete_prof_{row['profesor_id']}", on_click=open_modal, args=("delete_profesor", row['profesor_id']), use_container_width=True)

        profesor_renderers = {
            "Acciones": render_acciones_profesor,
            "Nombre Completo": lambda row: st.write(row['nombre_completo']),
            "Status": lambda row: st.write(row['status'])
        }

        display_data_table(df_profesores, [2, 6, 2], ["Acciones", "Nombre Completo", "Status"], profesor_renderers)
    except Exception as e:
        st.error(f"Error al cargar la lista de profesores: {e}")


# --- DEFINICIONES DE MODALES (Usando decorador @st.dialog) ---

@st.dialog("✏️ Editar Alumno")
def modal_editar_alumno(alumno_data, conn):
    
    # --- ¡NUEVA LÓGICA! ---
    # 1. Cargar grupos activos para el selectbox
    df_grupos_options = pd.read_sql("SELECT grupo_id, nombre_grupo FROM Grupos WHERE status_grupo = 'Activo' ORDER BY nombre_grupo ASC", conn)
    opciones_grupo = {0: "Sin Asignar"}
    opciones_grupo.update(pd.Series(df_grupos_options.nombre_grupo.values, index=df_grupos_options.grupo_id.astype(int)).to_dict())
    
    # 2. Buscar el grupo actual del alumno
    current_grupo_id = 0 # Por defecto "Sin Asignar"
    try:
        current_grupo_id = pd.read_sql(f"SELECT grupo_id FROM Inscripciones WHERE alumno_id = {int(alumno_data['alumno_id'])}", conn).iloc[0]['grupo_id']
    except IndexError:
        pass # El alumno no tiene grupo, se queda en 0
    
    # 3. Encontrar el índice correcto para el selectbox
    lista_ids_opciones = list(opciones_grupo.keys())
    current_index = lista_ids_opciones.index(current_grupo_id) if current_grupo_id in lista_ids_opciones else 0

    with st.form("edit_alumno_form"):
        st.subheader(f"Editando a: {alumno_data['nombre_completo']}")
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre", value=alumno_data["nombre_completo"])
            matricula = st.text_input("Matrícula", value=alumno_data["matricula"])
            correo = st.text_input("Correo", value=alumno_data["correo"])
            
            # --- ¡NUEVO CAMPO! ---
            nuevo_grupo_id = st.selectbox(
                "Asignar a Grupo", 
                options=lista_ids_opciones, 
                format_func=lambda x: opciones_grupo[x], 
                index=current_index
            )
            
        with col2:
            telefono = st.text_input("Teléfono", value=alumno_data["telefono"])
            estado = st.text_input("Estado de residencia", value=alumno_data["estado_residencia"])
            
            # Aseguramos que 'Finalizado' esté disponible
            status_list = ["Activo", "Baja", "Restringido", "Finalizado"]
            if alumno_data['status_alumno'] not in status_list:
                 status_list.append(alumno_data['status_alumno'])
            current_status_index = status_list.index(alumno_data['status_alumno'])
            
            status = st.selectbox("Status", status_list, index=current_status_index)
            fecha_nacimiento = st.date_input("Fecha de Nacimiento", value=pd.to_datetime(alumno_data["fecha_nacimiento"]))

        c1, c2 = st.columns(2)
        if c1.form_submit_button("Actualizar", type="primary", use_container_width=True):
            alumno_id_int = int(alumno_data["alumno_id"])
            with conn.cursor() as cur:
                # 1. Actualizar los datos del alumno
                sql_alumno = "UPDATE Alumnos SET nombre_completo=%s, status_alumno=%s, matricula=%s, correo=%s, telefono=%s, estado_residencia=%s, fecha_nacimiento=%s WHERE alumno_id=%s"
                cur.execute(sql_alumno, (nombre, status, matricula, correo, telefono, estado, fecha_nacimiento, alumno_id_int))
                
                # --- ¡NUEVA LÓGICA DE INSCRIPCIÓN! ---
                # 2. Borrar cualquier inscripción antigua
                cur.execute("DELETE FROM Inscripciones WHERE alumno_id = %s", (alumno_id_int,))
                
                # 3. Si se seleccionó un grupo nuevo, insertarlo
                if nuevo_grupo_id != 0:
                    cur.execute("INSERT INTO Inscripciones (alumno_id, grupo_id) VALUES (%s, %s)", (alumno_id_int, int(nuevo_grupo_id)))
                
                conn.commit()
            st.success("Alumno actualizado y grupo reasignado con éxito.")
            close_modal_and_rerun()
        if c2.form_submit_button("Cancelar", use_container_width=True):
            close_modal_and_rerun()

@st.dialog("✏️ Editar Grupo")
def modal_editar_grupo(grupo_data, conn):
    df_profesores_options = pd.read_sql("SELECT profesor_id, nombre_completo FROM Profesores WHERE status = 'Activo'", conn)
    with st.form("edit_grupo_form"):
        st.subheader(f"Editando Grupo: {grupo_data['nombre_grupo']}")
        
        nombre_grupo = st.text_input("Nombre del Grupo", value=grupo_data['nombre_grupo'])
        st.write("") # Espacio
        
        # 'Finalizado' se quita de las opciones de edición
        status_grupo = st.selectbox("Status", ["Activo", "Próximo"], index=["Activo", "Próximo"].index(grupo_data['status_grupo']) if grupo_data['status_grupo'] in ["Activo", "Próximo"] else 0)
        st.write("") # Espacio

        prof_index = df_profesores_options[df_profesores_options['profesor_id'] == grupo_data['profesor_id']].index
        prof_id_options = df_profesores_options['profesor_id']
        prof_id = st.selectbox("Profesor", options=prof_id_options, index=int(prof_index[0]) if len(prof_index) > 0 else 0, format_func=lambda x: df_profesores_options[df_profesores_options['profesor_id'] == x]['nombre_completo'].values[0])
        
        st.write("") # Espacio
        
        # --- ¡NUEVOS CAMPOS DE FECHA! ---
        col1, col2 = st.columns(2)
        with col1:
            fecha_inicio = st.date_input("Fecha de Inicio", value=pd.to_datetime(grupo_data["fecha_inicio"]))
        with col2:
            fecha_termino = st.date_input("Fecha de Término", value=pd.to_datetime(grupo_data["fecha_termino"]))
        # --- Fin de nuevos campos ---

        st.write("") # Espacio
        c1, c2 = st.columns(2)
        if c1.form_submit_button("Actualizar", type="primary", use_container_width=True):
            
            # --- ¡NUEVA LÓGICA! (Validaciones) ---
            valid = True
            today = datetime.date.today()

            if fecha_termino < fecha_inicio:
                st.error("Error: La Fecha de Término no puede ser anterior a la Fecha de Inicio.")
                valid = False
            
            # (No aplicamos la regla de 'Próximo' > 'hoy' al editar, 
            # ya que el admin podría estar corrigiendo un error)
            
            if valid:
                try:
                    with conn.cursor() as cur:
                        # Actualizamos la query para incluir las fechas
                        sql = """
                            UPDATE Grupos SET 
                            nombre_grupo=%s, status_grupo=%s, profesor_id=%s, 
                            fecha_inicio=%s, fecha_termino=%s 
                            WHERE grupo_id=%s
                        """
                        cur.execute(sql, (
                            nombre_grupo, status_grupo, int(prof_id), 
                            fecha_inicio, fecha_termino, 
                            int(grupo_data['grupo_id'])
                        ))
                        conn.commit()
                    st.success("Grupo actualizado.")
                    close_modal_and_rerun()
                except Exception as e:
                    st.error(f"Error al actualizar el grupo: {e}")
                    
        if c2.form_submit_button("Cancelar", use_container_width=True):
            close_modal_and_rerun()

@st.dialog("✅ Finalizar y Archivar Grupo")
def modal_finalizar_grupo(grupo_id, conn):
    st.warning(f"¿Estás seguro de que quieres finalizar el grupo ID {grupo_id}? Esta acción guardará un historial, marcará a los alumnos como 'Finalizado' y los desvinculará.")
    col1, col2 = st.columns(2)
    if col1.button("Confirmar Finalización", type="primary", use_container_width=True):
        try:
            with conn.cursor() as cur:
                grupo_id_int = int(grupo_id)
                
                # --- (SOLUCIÓN PROBLEMA 2) PASO 1: ACTUALIZAR ALUMNOS ---
                # Primero, marcamos a los alumnos 'Activos' de este grupo como 'Finalizado'
                st.write("Actualizando status de alumnos...") # Feedback visual
                cur.execute("""
                    UPDATE Alumnos a
                    SET status_alumno = 'Finalizado'
                    FROM Inscripciones i
                    WHERE a.alumno_id = i.alumno_id
                    AND i.grupo_id = %s
                    AND a.status_alumno = 'Activo';
                """, (grupo_id_int,))
                
                # PASO 2: Obtener datos para el historial
                st.write("Generando historial...")
                cur.execute("SELECT g.nombre_grupo, p.nombre_completo, g.fecha_inicio, g.fecha_termino FROM Grupos g JOIN Profesores p ON g.profesor_id = p.profesor_id WHERE g.grupo_id = %s", (grupo_id_int,))
                grupo_info = cur.fetchone()
                if not grupo_info:
                    st.error("No se encontró el grupo para finalizar.")
                else:
                    nombre_grupo, nombre_profesor, fecha_inicio, fecha_termino = grupo_info
                    df_alumnos_grupo = pd.read_sql("SELECT a.nombre_completo, a.matricula, a.status_alumno, a.certificado FROM Alumnos a JOIN Inscripciones i ON a.alumno_id = i.alumno_id WHERE i.grupo_id = %s", conn, params=(grupo_id_int,))
                    alumnos_list_final = [{'nombre': al['nombre_completo'], 'matricula': al['matricula'], 'status_final': al['status_alumno'], 'certificado': al['certificado']} for i, al in df_alumnos_grupo.iterrows()]
                    snapshot_json = json.dumps({"alumnos": alumnos_list_final}, indent=4, default=str)

                    # PASO 3: Insertar historial
                    cur.execute("INSERT INTO Grupos_Historial (nombre_grupo, nombre_profesor, datos_grupo_alumnos, fecha_inicio, fecha_termino) VALUES (%s, %s, %s, %s, %s)", (nombre_grupo, nombre_profesor, snapshot_json, fecha_inicio, fecha_termino))
                    
                    # PASO 4: Borrar inscripciones
                    st.write("Desvinculando alumnos...")
                    cur.execute("DELETE FROM Inscripciones WHERE grupo_id = %s", (grupo_id_int,))
                    
                    # PASO 5: Actualizar status del grupo
                    cur.execute("UPDATE Grupos SET status_grupo = 'Finalizado' WHERE grupo_id = %s", (grupo_id_int,))
                    
                    conn.commit()
                    st.success("Grupo finalizado y archivado con éxito.")
            close_modal_and_rerun()
        except Exception as e:
            st.error(f"Error al finalizar el grupo: {e}")
            conn.rollback() # Revertir cambios si algo falla
    if col2.button("Cancelar", use_container_width=True):
        close_modal_and_rerun()

@st.dialog("♻️ Restablecer Grupo")
def modal_restablecer_grupo(grupo_id, conn):
    df_profesores_options = pd.read_sql("SELECT profesor_id, nombre_completo FROM Profesores WHERE status = 'Activo'", conn)
    with st.form("reset_grupo_form"):
        st.info(f"Vas a reactivar el grupo finalizado ID {grupo_id}. Asigna un nuevo profesor y nuevas fechas.")
        profesor_id = st.selectbox("Asignar Nuevo Profesor", options=df_profesores_options['profesor_id'], format_func=lambda x: df_profesores_options.loc[df_profesores_options['profesor_id'] == x, 'nombre_completo'].iloc[0])
        nueva_fecha_inicio = st.date_input("Nueva Fecha de Inicio", value=datetime.date.today())
        nueva_fecha_termino = st.date_input("Nueva Fecha de Término", value=datetime.date.today() + datetime.timedelta(days=30))

        c1, c2 = st.columns(2)
        if c1.form_submit_button("Confirmar y Restablecer", use_container_width=True, type="primary"):
            with conn.cursor() as cur:
                sql = "UPDATE Grupos SET status_grupo = 'Activo', profesor_id = %s, fecha_inicio = %s, fecha_termino = %s WHERE grupo_id = %s"
                cur.execute(sql, (int(profesor_id), nueva_fecha_inicio, nueva_fecha_termino, int(grupo_id)))
                conn.commit()
            st.success("Grupo restablecido y activado con éxito.")
            close_modal_and_rerun()
        if c2.form_submit_button("Cancelar", use_container_width=True):
            close_modal_and_rerun()

@st.dialog("✏️ Editar Profesor")
def modal_editar_profesor(profesor_data, conn):
    with st.form("edit_profesor_form"):
        st.subheader(f"Editando a: {profesor_data['nombre_completo']}")
        nombre_profesor = st.text_input("Nombre Completo", value=profesor_data['nombre_completo'])
        status_profesor = st.selectbox("Status", ["Activo", "Inactivo"], index=["Activo", "Inactivo"].index(profesor_data['status']))
        
        c1, c2 = st.columns(2)
        if c1.form_submit_button("Actualizar", type="primary", use_container_width=True):
            with conn.cursor() as cur:
                sql = "UPDATE Profesores SET nombre_completo=%s, status=%s WHERE profesor_id=%s"
                cur.execute(sql, (nombre_profesor, status_profesor, int(profesor_data['profesor_id'])))
                conn.commit()
            st.success("Profesor actualizado.")
            close_modal_and_rerun()
        if c2.form_submit_button("Cancelar", use_container_width=True):
            close_modal_and_rerun()

@st.dialog("❌ Dar de Baja Profesor")
def modal_eliminar_profesor(profesor_id, conn):
    st.warning(f"¿Seguro que quieres dar de baja (marcar como 'Inactivo') al profesor con ID {profesor_id}?")
    col1, col2 = st.columns(2)
    if col1.button("Confirmar Baja", type="primary", use_container_width=True):
        with conn.cursor() as cur:
            cur.execute("UPDATE Profesores SET status='Inactivo' WHERE profesor_id=%s", (int(profesor_id),))
            conn.commit()
        st.success("Profesor dado de baja.")
        close_modal_and_rerun()
    if col2.button("Cancelar", use_container_width=True):
        close_modal_and_rerun()

# --- LÓGICA PRINCIPAL PARA INVOCAR MODALES ---
# Este bloque ahora "consume" el estado para evitar que los modales se reabran solos.

if "modal_tipo" in st.session_state and st.session_state.modal_tipo is not None:
    # 1. Lee el estado
    tipo = st.session_state.modal_tipo
    obj_id = st.session_state.modal_id
    conn = get_connection()

    # 2. Limpia el estado INMEDIATAMENTE
    # Esto evita que el modal se vuelva a abrir si el usuario usa un filtro
    st.session_state.modal_tipo = None
    st.session_state.modal_id = None

    # 3. Llama a la función del modal (que se dibujará esta única vez)
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
        st.error("Error: No se encontró el registro. Es posible que haya sido eliminado. Refrescando la página...")
        st.rerun() # Forzar un rerun si el ID no existe
    except Exception as e:
        st.error(f"Ocurrió un error al procesar el modal: {e}")