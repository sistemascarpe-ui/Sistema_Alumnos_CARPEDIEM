import streamlit as st

def load_dark_mode_css():
    st.markdown("""
    <style>
    :root {
        --primary-color-dark: #1DB954;
        --background-color-dark: #1A1A2E;
        --secondary-background-color-dark: #16213E;
        --text-color-dark: #E0E0E0;
        --sidebar-background-dark: #0F3460;
        --sidebar-text-dark: #E0E0E0;
        --header-background-dark: #16213E;
        --header-text-dark: #E0E0E0;
        --tab-active-text-dark: #1DB954;
        --tab-active-line-dark: #1DB954;
        --tab-inactive-text-dark: #A0A0A0;
        --card-background-dark: #16213E;
        --card-border-dark: #0F3460;
        --input-text-color-dark: #E0E0E0;
        --input-background-color-dark: #2C3E50;
        --input-border-color-dark: #0F3460;
    }

    /* AÑADIDO: Regla para ocultar la navegación de páginas (faltaba) */
    [data-testid="stSidebar"] [data-testid="stSidebarNavItems"] {
        display: none !important;
    }

    body, .stApp {
        background-color: var(--background-color-dark) !important;
        color: var(--text-color-dark) !important;
        transition: background-color 0.3s, color 0.3s;
        text-align: center !important; /* AÑADIDO: Alineación central (faltaba) */
    }

    /* ================================================================== */
    /* === 1. CONFIGURACIÓN GENERAL Y MENÚ DOBLE FIX === */
    /* ================================================================== */

    .stApp {
        font-family: 'Segoe UI', Tahoma, sans-serif !important;
        padding: 1.2rem !important;
        max-width: 100% !important;
        margin: 0 auto !important;
    }
    h1, h2, h3, h4, h5, h6 {
        text-align: center !important;
        color: var(--text-color-dark) !important;
        transition: color 0.3s;
    }
    [data-testid="stTable"], [data-testid="stDataFrame"] {
        margin-left: auto !important;
        margin-right: auto !important;
        display: block !important;
    }

    div[data-testid="stForm"], div[data-testid="stForm"] * {
        text-align: left !important;
    }

    div[data-baseweb="select"] div, div[data-baseweb="select"] input {
        text-align: left !important;
    }
    div[data-testid="stForm"] div[data-testid="stTextInput"],
    div[data-testid="stForm"] div[data-testid="stDateInput"],
    div[data-testid="stForm"] div[data-testid="stSelectbox"] {
        text-align: left !important;
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
    
    div[data-baseweb="tab-list"] {
    border-bottom: 2px solid var(--primary-color-dark) !important;
    margin-bottom: 0 !important;
    justify-content: center !important;
    width: 100% !important;
}

    
    button[data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        border-bottom: 3px solid transparent !important;
        padding: 0.75rem 1.5rem !important;
        margin: 0 !important;
        color: var(--tab-inactive-text-dark) !important;
        transition: all 0.2s ease !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        position: relative;
        border-right: 1px solid var(--card-border-dark);
        outline: none !important;
        box-shadow: none !important;
    }

    button[data-baseweb="tab"]:last-of-type {
        border-right: none !important;
    }

div[data-baseweb="tab-highlight"] {
    display: none !important;
}

button[data-baseweb="tab"][aria-selected="true"]::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background-color: var(--tab-active-line-dark); /* Color de la línea de resaltado */
}
    
    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--tab-active-text-dark) !important;
        border: none !important;
    }

    div[aria-label*="Filtrar por Grupo"],
    div[aria-label*="Selecciona un Alumno"] {
        width: 50% !important;
        height: auto !important;
        max-width: none !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
        margin: inherit !important;
        padding: inherit !important;
    }

    /* --- (Resto de Sección 2) --- */
    .main-header {
        background-color: var(--header-background-dark) !important;
        padding: 2.5rem !important;
        border-radius: 12px !important;
        color: var(--header-text-dark) !important;
        text-align: center !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        margin-bottom: 2rem !important;
        width: 100% !important;
        max-width: 100% !important;
        transition: background-color 0.3s, color 0.3s;
    }
    .main-header h1 { font-size: 2.5rem; font-weight: bold; margin: 0; }
    .main-header p { font-size: 1.2rem; font-weight: 300; opacity: 0.9; margin-top: 0.5rem; }

    [data-testid="stSidebar"] {
        background-color: var(--sidebar-background-dark) !important;
        color: var(--sidebar-text-dark) !important;
        border-radius: 0 12px 12px 0 !important;
        padding: 1rem !important;
        box-shadow: 2px 0 10px rgba(0,0,0,0.1) !important;
        transition: background-color 0.3s, color 0.3s;
    }
    [data-testid="stSidebar"] * {
        color: var(--sidebar-text-dark) !important;
        transition: color 0.3s;
    }


    /* Floating Card Style */
    .floating-card {
        background-color: var(--card-background-dark);
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid var(--card-border-dark);
        width: 100% !important;
        max-width: 100% !important;
        transition: background-color 0.3s, border-color 0.3s;
    }
    /* Media queries para responsividad (SIN CAMBIOS) */
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
            font-size: 2.5rem;
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
        [data-testid="stForm"] {
            padding: 0.8rem !important;
        }
        [data-testid="stSidebar"] {
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
            margin-bottom: 1rem !important;
            border-radius: 12px !important;
        }
        
        button {
            width: 100% !important;
            margin-bottom: 0.5rem !important;
        }
        
        input, select, textarea {
            font-size: 16px !important;
        }
        
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
        border: 1px solid var(--card-border-dark);
        padding: 1.5rem !important;
        background-color: var(--card-background-dark);
        margin-bottom: 1.5rem;
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: auto !important;
        transition: background-color 0.3s, border-color 0.3s;
    }
    [data-testid="stExpander"] > summary {
        font-weight: 600;
        border: none;
        color: var(--text-color-dark);
    }
    [data-testid="stExpander"] > summary:hover {
        color: var(--tab-active-text-dark);
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        border-radius: 8px !important;
        border: 1px solid var(--input-border-color-dark) !important;
        padding: 0.4rem 0.6rem !important;
        background-color: var(--input-background-color-dark) !important;
        color: var(--input-text-color-dark) !important;
        transition: background-color 0.3s, color 0.3s, border-color 0.3s;
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
        div[data-baseweb="select"] > div:first-child {
            width: 50% !important;
        }
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
        /* ¡¡CORREGIDO!! Usando tu variable verde en lugar de azul */
        border: 2px solid var(--primary-color-dark) !important; 
        transition: all 0.2s ease !important;
    }
    button:hover {
        /* ¡¡CORREGIDO!! Usando un verde más brillante para hover en lugar de naranja */
        border-color: #2EE06C !important; 
    }
    button[data-baseweb="tab"]:hover {
        border-color: transparent !important;
        border-bottom-color: var(--primary-color-dark) !important;
    }
    
    /* --- BOTÓN AZUL SÓLIDO (PRIMARY) --- */
    /* ¡¡SECCIÓN ENTERA CORREGIDA!! */
    button[kind="primary"], button[kind="primaryFormSubmit"] {
        background-color: var(--primary-color-dark) !important; /* Usando tu verde */
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    button[kind="primary"]:hover, button[kind="primaryFormSubmit"]:hover {
        background-color: #189a44 !important; /* Un verde más oscuro para hover */
    }

    /* ================================================================== */
    /* === 5. RESPONSIVIDAD GENERAL Y ALINEACIÓN DE TABLAS === */
    /* ================================================================== */
    [data-testid="stDataFrame"] {
        width: 100% !important;
        overflow-x: auto !important;
        display: block !important;
        border: 2px solid var(--primary-color-dark) !important;
        border-radius: 10px !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.15) !important;
        margin-bottom: 2rem !important;
        text-align: center !important;
    }
    
    [data-testid="stDataFrame"] table th,
    [data-testid="stDataFrame"] table td {
        border: 1px solid var(--card-border-dark) !important;
        padding: 12px 18px !important;
        text-align: center !important;
        vertical-align: middle !important;
        color: var(--text-color-dark) !important;
    }

    [data-testid="stDataFrame"] table th {
        background-color: var(--primary-color-dark) !important;
        color: white !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        text-align: center !important;
    }

    [data-testid="stDataFrame"] table th > div,
    [data-testid="stDataFrame"] table td > div,
    [data-testid="stDataFrame"] table th .stMarkdownContainer,
    [data-testid="stDataFrame"] table td .stMarkdownContainer,
    .tabla-estilizada th > div,
    .tabla-estilizada td > div,
    .tabla-estilizada th .stMarkdownContainer,
    .tabla-estilizada td .stMarkdownContainer {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        height: 100% !important;
    }

    [data-testid="stDataFrame"] table tbody tr:nth-child(even) {
        background-color: var(--secondary-background-color-dark) !important;
    }

    [data-testid="stDataFrame"] table tbody tr:hover {
        background-color: #2C3E50 !important;
        cursor: pointer !important;
    }
    
    @media (max-width: 768px) {
        [data-testid="stDataFrame"] table {
            font-size: 0.9rem !important;
        }
        [data-testid="stDataFrame"] th,
        [data-testid="stDataFrame"] td {
            padding: 0.6rem !important;
        }
    }
    
    [data-testid="stDataFrame"] table {
        width: 100% !important;
    }
    
    [data-testid="stDataFrame"] .stMarkdownContainer,
    [data-testid="stDataFrame"] .stVerticalBlock div[data-testid="stMarkdownContainer"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
    }

    [data-testid="stDataFrame"] td > div,
    .tabla-estilizada td > div {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        height: 100% !important;
    }

    .styled-dataframe {
        border: 1px solid var(--card-border-dark) !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
        overflow: hidden !important;
    }

    .styled-dataframe table {
        width: 100% !important;
        border-collapse: collapse !important;
    }

    .styled-dataframe th {
        background-color: var(--sidebar-background-dark) !important;
        font-weight: bold !important;
        color: var(--sidebar-text-dark) !important;
        padding: 10px 15px !important;
        text-align: center !important;
        border: 1px solid var(--card-border-dark) !important;
    }

    .styled-dataframe td {
        padding: 8px 15px !important;
        text-align: center !important;
        border: 1px solid var(--card-border-dark) !important;
        color: var(--text-color-dark) !important;
    }

    .styled-dataframe tbody tr:nth-child(even) {
        background-color: var(--secondary-background-color-dark) !important;
    }

    .styled-dataframe tbody tr:hover {
        background-color: #2C3E50 !important;
    }

    img {
        max-width: 100% !important;
        height: auto !important;
    }

    .restricted-span {
        letter-spacing: 0.05em !important;
        white-space: nowrap !important;
        padding: 0 2px !important;
    }

    /* ================================================================== */
    /* === 6. ALINEACIÓN DE BOTONES E INPUTS === */
    /* ================================================================== */
    .st-emotion-cache-1r6slb0 > div > div:has(div[data-testid="stTextInput"]) + div[data-testid="stButton"] {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .st-emotion-cache-1r6slb0 > div > div:has(div[data-testid="stTextInput"]) {
        flex-grow: 1;
    }

    [data-testid="stFormSubmitHint"] {
        display: none !important;
    }

    /* ================================================================== */
    /* === 7. ESTILOS PARA TABLAS HTML (.tabla-estilizada terminada) === */
    /* ================================================================== */

    .tabla-estilizada {
        width: 100%;
        border-collapse: collapse;
        margin: 2rem 0;
        font-size: 0.95em;
        font-family: 'Segoe UI', Tahoma, sans-serif;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        overflow: hidden;
        border: 1px solid var(--card-border-dark);
    }

    .tabla-estilizada thead tr {
        background-color: var(--sidebar-background-dark);
        color: #ffffff;
        text-align: center;
        font-weight: 600;
    }

    .tabla-estilizada th,
    .tabla-estilizada td {
        padding: 12px 15px;
        text-align: center;
        color: var(--text-color-dark);
    }

    .tabla-estilizada tbody tr {
        border-bottom: 1px solid var(--card-border-dark);
    }

    .tabla-estilizada tbody tr:nth-of-type(even) {
        background-color: var(--secondary-background-color-dark);
    }

    .tabla-estilizada tbody tr:last-of-type {
        border-bottom: 2px solid var(--sidebar-background-dark);
    }

    .tabla-estilizada tbody tr:hover {
        background-color: #2C3E50;
        cursor: default;
    }

    /* ================================================================== */
    /* ================================================================== */
    /* === 8. CSS PARA EL BOTÓN "VOLVER ARRIBA" (SIEMPRE VISIBLE) === */
    /* ================================================================== */

    #back-to-top {
        position: fixed;
        bottom: 20px;
        right: 30px;
        z-index: 9999;
        border: none;
        outline: none;
        background-color: #1DB954; /* Color de botón para dark mode */
        color: white;
        cursor: pointer;
        padding: 15px;
        border-radius: 10px;
        font-size: 18px;
        height: 50px;
        width: 50px;
        text-align: center;
        line-height: 20px;
        
        display: block !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    #back-to-top:hover {
        background-color: #159040; /* Color hover para dark mode */
    }
    </style>
    """, unsafe_allow_html=True)