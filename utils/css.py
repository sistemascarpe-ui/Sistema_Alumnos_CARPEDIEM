import streamlit as st

def load_css():
    st.markdown("""
    <style>
    [data-testid="stSidebarNavItems"] {
        display: none;
    }

    /* ================================================================== */
    /* === 1. CONFIGURACIÓN GENERAL Y MENÚ DOBLE FIX === */
    /* ================================================================== */


    body {
        background-color: #f0f4f8;
    }
    .stApp {
        background-color: #f0f4f8 !important;
        color: #343a40 !important;
        font-family: 'Segoe UI', Tahoma, sans-serif !important;
        padding: 1.2rem !important;
        max-width: 100% !important;
        margin: 0 auto !important;
    }
    [data-testid="stBlock"] > div:first-child {
        background-color: transparent !important;
        padding: 0 !important;
        width: 100% !important;
    }
    .st-emotion-cache-1y4p8pa {
        background-color: transparent !important;
    }

    /* ================================================================== */
    /* === 2. ESTILOS DE PESTAÑAS (TABS) - ¡¡MEJORADO!! === */
    /* ================================================================== */
    
    /* El contenedor de las pestañas */
    div[data-baseweb="tab-list"] {
    border-bottom: 2px solid #0d47a1 !important; /* Línea base azul marino */
    margin-bottom: 0 !important; /* Eliminado el margen inferior */
    justify-content: center !important; /* ¡¡CENTRADO!! */
    width: 100% !important;
}

    
    /* Cada pestaña (botón) */
    button[data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        border-bottom: 3px solid transparent !important; /* Grosor base */
        padding: 0.75rem 1.5rem !important; /* Más espaciado */
        margin: 0 !important;
        color: #6c757d !important;
        transition: all 0.2s ease !important;
        font-size: 1.1rem !important; /* Tamaño ajustado */
        font-weight: 600 !important;
        position: relative;
        border-right: 1px solid #d0d7de; /* LÍNEA DIVISORA DERECHA */
        outline: none !important;
        box-shadow: none !important;
    }

    /* Quitar borde a la última pestaña */
    button[data-baseweb="tab"]:last-of-type {
        border-right: none !important;
    }

div[data-baseweb="tab-highlight"] {
    display: none !important; /* Oculta el resaltado predeterminado de Streamlit */
}

button[data-baseweb="tab"][aria-selected="true"]::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background-color: #FF8400; /* Color de la línea de resaltado */
}
    
    /* Pestaña SELECCIONADA */
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #0d47a1 !important; /* ¡¡TEXTO AZUL MARINO!! */
        border: none !important; /* Eliminar todos los bordes */
    }
    
    /* --- (Resto de Sección 2) --- */
    .main-header {
        background-color: #0d47a1 !important;
        padding: 2.5rem !important;
        border-radius: 12px !important;
        color: white !important;
        text-align: center !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        margin-bottom: 2rem !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    .main-header h1 { font-size: 2.5rem; font-weight: bold; margin: 0; }
    .main-header p { font-size: 1.2rem; font-weight: 300; opacity: 0.9; margin-top: 0.5rem; }

    [data-testid="stSidebar"] {
        background-color: #0d47a1 !important;
        color: white !important;
        border-radius: 0 12px 12px 0 !important;
        padding: 1rem !important;
        box-shadow: 2px 0 10px rgba(0,0,0,0.1) !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }


    /* Floating Card Style */
    .floating-card {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid #e0e0e0;
        width: 100% !important;
        max-width: 100% !important;
    }
    /* Media queries para responsividad */
    @media (max-width: 1200px) {
        .stApp {
            padding: 1rem !important;
        }
        .main-header {
            padding: 2rem !important;
        }
        .main-header h1 { 
            font-size: 2.2rem; 
        }
    }
    
    @media (max-width: 992px) {
        .main-header h1 { 
            font-size: 2rem; 
        }
        .main-header p { 
            font-size: 1.1rem; 
        }
    }
    
    @media (max-width: 768px) {
        .stApp {
            padding: 0.5rem !important;
        }
        .floating-card {
            padding: 1rem !important;
        }
        .main-header {
            padding: 1.5rem !important;
        }
        .main-header h1 { 
            font-size: 1.8rem; 
        }
        .main-header p { 
            font-size: 1rem; 
        }
        /* Mejora para tablas en móviles */
        [data-testid="stTable"], [data-testid="stDataFrame"] {
            font-size: 0.9rem !important;
        }
    }
    
    @media (max-width: 576px) {
        .stApp {
            padding: 0.3rem !important;
        }
        .main-header {
            padding: 1rem !important;
            margin-bottom: 1rem !important;
        }
        .main-header h1 { 
            font-size: 1.5rem; 
        }
        .main-header p { 
            font-size: 0.9rem; 
            margin-top: 0.3rem;
        }
        /* Ajustes para formularios en móviles */
        [data-testid="stForm"] {
            padding: 0.8rem !important;
        }
        /* Optimizaciones para dispositivos móviles */
        /* Ajustes para el sidebar en móviles */
        [data-testid="stSidebar"] {
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
            margin-bottom: 1rem !important;
            border-radius: 12px !important;
        }
        
        /* Ajustes para botones en móviles */
        button {
            width: 100% !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Ajustes para inputs en móviles */
        input, select, textarea {
            font-size: 16px !important; /* Evita zoom en iOS */
        }
        
        /* Ajustes para los encabezados */
        h1, h2, h3 {
            text-align: center !important;
        }
    }



    /* ================================================================== */
    /* === 3. FORMULARIOS, EXPANDERS Y FILTROS === */
    /* ================================================================== */
    [data-testid="stExpander"], [data-testid="stForm"], .st-emotion-cache-1r6slb0 {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        padding: 1.5rem !important;
        background-color: white;
        margin-bottom: 1.5rem;
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: auto !important;
    }
    [data-testid="stExpander"] > summary {
        font-weight: 600;
        border: none;
    }
    [data-testid="stExpander"] > summary:hover {
        color: #0d47a1;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        border-radius: 8px !important;
        border: 1px solid #dfe1e5 !important;
        padding: 0.4rem 0.6rem !important;
        background-color: white !important;
    }
    div[data-testid="stSelectbox"] {
        width: 100% !important;
        height: auto !important;
        min-height: 40px !important;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        width: 100% !important;
        height: 40px !important;
        min-height: 40px !important;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        width: 100% !important;
        height: 40px !important;
        min-height: 40px !important;
        display: flex !important;
        align-items: center !important;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div > div {
        font-size: 14px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        height: auto !important;
    }
    div[data-baseweb="popover"] { z-index: 10000 !important; }

    /* ================================================================== */
    /* === 4. BOTONES (¡¡ESTILO GHOST ACTUALIZADO!!) === */
    /* ================================================================== */
    
    button {
        border: 2px solid #1500FF !important; /* Borde inicial */
        transition: all 0.2s ease !important;
    }
    button:hover {
        border-color: #FF8400 !important; /* Borde al pasar el cursor */
    }
    button[data-baseweb="tab"]:hover {
        border-color: transparent !important; /* Asegura que otros bordes sean transparentes */
        border-bottom-color: #0d47a1 !important; /* Borde inferior azul al pasar el cursor en pestañas */
    }
    /* --- BOTÓN AZUL SÓLIDO (PRIMARY) --- */
    /* Se usa con type="primary" en st.button o st.form_submit_button */
    /* Perfecto */
    button[kind="primary"], button[kind="primaryFormSubmit"] {
        background-color: #000896 !important; /* Nuevo Azul */
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    button[kind="primary"]:hover, button[kind="primaryFormSubmit"]:hover {
        background-color: #00067A !important; /* Azul más oscuro al hover */
    }

    /* ================================================================== */
    /* === 5. RESPONSIVIDAD GENERAL Y ALINEACIÓN DE TABLAS === */
    /* ================================================================== */
    /* Mejoras de responsividad para tablas */
    [data-testid="stTable"], [data-testid="stDataFrame"] {
        width: 100% !important;
        overflow-x: auto !important;
        display: block !important;
    }
    
    /* Asegurar que las tablas se ajusten al contenedor */
    .stTable, .stDataFrame {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Ajustar el tamaño de texto en tablas para dispositivos pequeños */
    @media (max-width: 768px) {
        .stTable table, .stDataFrame table {
            font-size: 0.9rem !important;
        }
        .stTable th, .stDataFrame th,
        .stTable td, .stDataFrame td {
            padding: 0.4rem !important;
        }
    }
    
    /* Alineación vertical de contenido en tablas */
    div[data-testid="stTable"] table {
        width: 100% !important;
    }
    
    div[data-testid="stTable"] th, div[data-testid="stTable"] td {
        vertical-align: middle !important;
        padding: 8px 12px !important;
        text-align: center !important;
    }
    
    /* Estilo para los botones de acción en tablas */
    div[data-testid="stTable"] button {
        margin: 0 auto !important;
        display: block !important;
    }
    
    /* Centrar contenido de los encabezados de tabla */
    .stMarkdownContainer {
        text-align: center !important;
    }
    
    .stVerticalBlock div[data-testid="stMarkdownContainer"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    /* Asegura que las imágenes no desborden su contenedor */
    img {
        max-width: 100% !important;
        height: auto !important;
    }

    /* ================================================================== */
    /* === 6. ALINEACIÓN DE BOTONES E INPUTS === */
    /* ================================================================== */
    .st-emotion-cache-1r6slb0 > div > div:has(div[data-testid="stTextInput"]) + div[data-testid="stButton"] {
        display: flex;
        align-items: center;
        gap: 10px; /* Espacio entre el input y el botón */
    }

    .st-emotion-cache-1r6slb0 > div > div:has(div[data-testid="stTextInput"]) {
        flex-grow: 1;
    }

    </style>
    """, unsafe_allow_html=True)