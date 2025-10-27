import streamlit as st

def load_css():
    st.markdown("""
    <style>
        /* Oculta la navegación nativa de Streamlit basada en archivos */
        [data-testid="stSidebarNavItems"] {
            display: none;
        }
        /* --- Fondo general blanco --- */
        .stApp {
            background-color: #ffffff !important;
            color: #343a40 !important;
            font-family: 'Segoe UI', Tahoma, sans-serif !important;
            padding: 1.2rem !important;
        }

        /* --- Encabezado principal azul con letras blancas --- */
        .main-header {
            background-color: #0d47a1 !important; /* Azul marino */
            padding: 1.5rem !important;
            border-radius: 12px !important;
            color: white !important;
            text-align: center !important;
            font-size: 1.8rem !important;
            font-weight: bold !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
            margin-bottom: 2rem !important;
        }

        /* --- Sidebar azul marino --- */
        [data-testid="stSidebar"] {
            background-color: #0d47a1 !important;
            color: white !important;
            border-radius: 0 12px 12px 0 !important;
            padding: 1rem !important;
            box-shadow: 2px 0 10px rgba(0,0,0,0.1) !important;
        }

        /* === MEJORAS DE ALINEACIÓN Y ESPACIADO === */
        
        /* Contenedores de filtros mejor alineados */
        .filter-container {
            display: flex;
            align-items: flex-end; /* Alinea por la parte inferior */
            gap: 1rem;
            margin-bottom: 1rem;
        }

        /* Alineación mejorada para bloques horizontales */
        div[data-testid="stHorizontalBlock"] {
            align-items: flex-end !important;
            gap: 1rem !important;
            margin-bottom: 1rem !important;
        }

        /* Mejor alineación para selectboxes en filtros */
        div[data-testid="stHorizontalBlock"] div[data-testid="stSelectbox"] {
            margin-bottom: 0 !important;
        }

        /* Alineación para campos de texto en filtros */
        div[data-testid="stHorizontalBlock"] div[data-testid="stTextInput"] {
            margin-bottom: 0 !important;
        }

        /* Espaciado consistente entre secciones */
        .stTabs > div > div > div > div {
            padding: 1rem 0 !important;
        }

        /* Mejor espaciado para expanders */
        div[data-testid="stExpander"] {
            margin-bottom: 1.5rem !important;
        }

        /* Alineación mejorada para formularios */
        div[data-testid="stForm"] {
            margin-bottom: 2rem !important;
        }

        /* Espaciado entre columnas en formularios */
        div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] {
            gap: 2rem !important;
        }

        /* --- Texto dentro del sidebar --- */
        [data-testid="stSidebar"] * {
            color: white !important;
        }

        /* --- Formularios --- */
        div[data-testid="stForm"] {
            background-color: #ffffff !important;
            padding: 1.5rem !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06) !important;
            margin-bottom: 1rem !important;
        }

        /* --- Inputs --- */
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stSelectbox"] select {
            border-radius: 8px !important;
            border: 1px solid #dfe1e5 !important;
            padding: 0.4rem !important;
        }

        /* --- Botones primarios --- */
        button[kind="primary"] {
            background-color: #1565c0 !important; /* Azul más fuerte */
            color: white !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
            border: none !important;
            transition: all 0.2s ease-in-out !important;
        }

        button[kind="primary"]:hover {
            background-color: #0d47a1 !important;
            transform: translateY(-2px) !important;
        }

        /* === TABLAS CON GRID DE LÍNEAS CLARAS === */
        
        /* Contenedor principal de datos */
        .stDataFrame {
            background-color: #ffffff !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06) !important;
            padding: 0.5rem !important;
        }

        .stDataFrame tr:hover {
            background-color: #e3f2fd !important;
        }

        /* Líneas verticales entre columnas en todas las tablas */
        div[data-testid="stHorizontalBlock"] > div {
            border-right: 1px solid #dee2e6 !important;
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
        }

        /* Quitar borde en la última columna */
        div[data-testid="stHorizontalBlock"] > div:last-child {
            border-right: none !important;
        }

        /* Líneas horizontales entre filas */
        div[data-testid="stHorizontalBlock"] {
            border-bottom: 1px solid #e9ecef !important;
            padding-top: 0.5rem !important;
            padding-bottom: 0.5rem !important;
        }

        /* Encabezados con fondo gris suave */
        .table-header-row {
            background-color: #f8f9fa !important;
            border-bottom: 2px solid #dee2e6 !important;
            padding: 0.75rem 0 !important;
            margin-bottom: 0 !important;
        }

        /* Espaciado consistente en tablas */
        div[data-testid="stHorizontalBlock"] {
            margin-bottom: 0 !important;
            gap: 0 !important;
        }

        /* Reducir padding en componentes de Streamlit para tablas compactas */
        div[data-testid="stColumn"] > div > div {
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }


        /* 1. Fondo general de la aplicación */
        body {
            background-color: #f0f2f6; /* Un gris muy claro para que resalten los elementos blancos */
        }

        /* 2. Tarjetas con Sombra (para los expanders, formularios y contenedores) */
        /* Seleccionamos los contenedores de Streamlit para aplicarles el estilo de tarjeta */
        [data-testid="stExpander"], 
        [data-testid="stForm"],
        .st-emotion-cache-1r6slb0 { /* Este es el contenedor de la tabla */
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-radius: 12px;
            border: 1px solid rgba(0,0,0,0.05); /* Un borde muy sutil */
            padding: 1rem;
            background-color: white;
        }

        /* 3. Botones con más "pop" */
        div[data-testid="stButton"] > button {
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.2s ease-in-out; /* Animación suave */
            border-width: 1px;
        }

        /* Efecto al pasar el cursor sobre un botón */
        div[data-testid="stButton"] > button:hover {
            transform: translateY(-2px); /* El botón "salta" un poco */
            box-shadow: 0 4px 8px rgba(0,0,0,0.15); /* La sombra se hace más grande */
        }

        /* 4. Quitar el borde por defecto del expander para que se vea más limpio */
        [data-testid="stExpander"] > summary {
            border: none;
        }

        /* === MEJORAS PARA MODALES === */
        
        /* Modales con mejor espaciado */
        div[data-testid="stModal"] {
            padding: 2rem !important;
        }

        div[data-testid="stModal"] > div {
            border-radius: 16px !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;
        }

        /* Mejor espaciado en formularios de modal */
        div[data-testid="stModal"] div[data-testid="stForm"] {
            padding: 1.5rem !important;
            margin-bottom: 1rem !important;
        }

        /* === SEPARADORES VISUALES === */
        
        .section-divider {
            border-top: 2px solid #e9ecef;
            margin: 2rem 0 1.5rem 0;
            padding-top: 1.5rem;
        }

        .group-separator {
            background: linear-gradient(90deg, #0d47a1 0%, #1565c0 100%);
            height: 3px;
            border-radius: 1.5px;
            margin: 1.5rem 0 1rem 0;
        }

        /* === PESTAÑAS SIN RECUADRO NARANJA === */
        
        /* NO ocultar el contenido de las pestañas */
        div[data-testid="stTabs"] > div > div > div {
            display: block !important;
            visibility: visible !important;
        }
        
        /* Anular cualquier fondo naranja/rojo en el indicador de tabs */
        div[data-testid="stTabs"] > div > div > div > div {
            background-color: transparent !important;
            background: transparent !important;
        }

        /* Contenedor de tabs limpio */
        div[data-baseweb="tab-list"] {
            background-color: transparent !important;
            padding: 0 !important;
            border-bottom: 1px solid #e9ecef !important;
            margin-bottom: 1.5rem !important;
        }

        /* Pestañas inactivas - blancas con borde gris */
        button[data-baseweb="tab"] {
            background-color: white !important;
            background: white !important;
            border: 2px solid #e9ecef !important;
            border-radius: 8px !important;
            padding: 0.75rem 1.5rem !important;
            margin: 0 0.5rem !important;
            font-size: 1.1rem !important;
            font-weight: normal !important;
            color: #6c757d !important;
            transition: all 0.2s ease !important;
            position: relative !important;
        }

        /* Pestaña activa - SOLO contorno naranja, letras grandes naranjas, SIN fondo naranja */
        button[data-baseweb="tab"][aria-selected="true"] {
            background-color: white !important;
            background: white !important;
            border: 2px solid #FF9500 !important;
            border-radius: 8px !important;
            color: #FF9500 !important;
            font-weight: 700 !important;
            font-size: 1.4rem !important;
            z-index: 1 !important;
        }

        /* Forzar que NO haya ningún fondo coloreado en ningún elemento interno de la pestaña activa */
        button[data-baseweb="tab"][aria-selected="true"] * {
            background-color: transparent !important;
            background: transparent !important;
        }

        /* Espesíficamente anular cualquier div con fondo */
        button[data-baseweb="tab"][aria-selected="true"] > div,
        button[data-baseweb="tab"][aria-selected="true"] > div > div,
        button[data-baseweb="tab"][aria-selected="true"] > div > div > div {
            background: none !important;
            background-color: transparent !important;
        }

        /* Hover en pestañas inactivas */
        button[data-baseweb="tab"]:hover:not([aria-selected="true"]) {
            color: #495057 !important;
            background-color: #f8f9fa !important;
            border-color: #dee2e6 !important;
        }
    </style>
    """, unsafe_allow_html=True)
