import streamlit as st

def load_css():
    st.markdown("""
    <style>
    /* ================================================================== */
    /* === 1. CONFIGURACIÓN GENERAL Y MENÚ DOBLE FIX === */
    /* ================================================================== */
    [data-testid="stSidebarNavItems"] { display: none; }

    body {
        background-color: #f0f4f8;
    }
    .stApp {
        background-color: #f0f4f8 !important;
        color: #343a40 !important;
        font-family: 'Segoe UI', Tahoma, sans-serif !important;
        padding: 1.2rem !important;
    }
    [data-testid="stBlock"] > div:first-child {
        background-color: transparent !important;
        padding: 0 !important;
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
    }

    /* Quitar borde a la última pestaña */
    button[data-baseweb="tab"]:last-of-type {
        border-right: none !important;
    }
    
    /* Pestaña SELECCIONADA */
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #0d47a1 !important; /* ¡¡TEXTO AZUL MARINO!! */
        border-bottom: 3px solid transparent !important; /* ¡¡LÍNEA AZUL MARINO!! */
    }
    
    /* --- (Resto de Sección 2) --- */
    .main-header {
        background-color: #0d47a1 !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        color: white !important;
        text-align: center !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        margin-bottom: 2rem !important;
    }
    .main-header h1 { font-size: 2rem; font-weight: bold; margin: 0; }
    .main-header p { font-size: 1rem; font-weight: 300; opacity: 0.9; margin-top: 0.25rem; }

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
    
    /* --- BOTÓN AZUL SÓLIDO (PRIMARY) --- */
    /* Se usa con type="primary" en st.button o st.form_submit_button */
    /* Perfecto para Login, Registro, Logout (como pediste) */
    button[kind="primary"] {
        background-color: #1565c0 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    button[kind="primary"]:hover {
        background-color: #0d47a1 !important;
    }

    /* --- BOTÓN GRIS SÓLIDO (SECONDARY) --- */
    /* Se usa con type="secondary". Bueno para 'Cancelar' en modales peligrosos */
    button[kind="secondary"] {
        background-color: #6c757d !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    button[kind="secondary"]:hover {
        background-color: #5a6268 !important;
    }
    
    /* --- NUEVOS BOTONES "GHOST" (Transparentes + Hover) --- */
    /* MODO DE USO en Python:
       st.markdown('<div class="btn-warning">', unsafe_allow_html=True)
       st.button("Editar", use_container_width=True)
       st.markdown('</div>', unsafe_allow_html=True)
    */

    /* Base para botones ghost (afecta a st.button Y st.form_submit_button) */
    .btn-success button,
    .btn-warning button,
    .btn-danger button {
        background-color: transparent !important;
        border-width: 2px !important;
        border-style: solid !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 0.4rem 1rem !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* VERDE (Success) - Restablecer, Actualizar */
    .btn-success button {
        border-color: #28a745 !important;
        color: #28a745 !important;
    }
    .btn-success button:hover,
    .btn-success button:focus {
        background-color: #28a745 !important;
        color: white !important;
    }

    /* AMARILLO (Warning) - Editar */
    .btn-warning button {
        border-color: #ffc107 !important;
        color: #ffc107 !important;
    }
    .btn-warning button:hover,
    .btn-warning button:focus {
        background-color: #ffc107 !important;
        color: #212529 !important; /* Texto oscuro para hover amarillo */
    }

    /* ROJO (Danger) - Finalizar, Baja, Cancelar */
    .btn-danger button {
        border-color: #dc3545 !important;
        color: #dc3545 !important;
    }
    .btn-danger button:hover,
    .btn-danger button:focus {
        background-color: #dc3545 !important;
        color: white !important;
    }

    /* Estilo específico para el botón de login */
    .login-form-container button[kind="primary"] {
        background-color: #1565c0 !important;
        color: white !important;
        border: none !important;
    }
    .login-form-container button[kind="primary"]:hover {
        background-color: #0d47a1 !important;
    }
    
    /* ================================================================== */
    /* === 5. ESTILO DE TABLA (GRID CLÁSICO SIMPLE) === */
    /* ================================================================== */

    /* --- (A) El "div" contenedor principal de la tabla --- */
    .table-container {
        background-color: #ffffff;      /* Fondo blanco */
        border: 1px solid #e0e0e0;   /* Un solo borde exterior */
        border-radius: 12px;            /* Esquinas redondeadas para el contenedor */
        box-shadow: 0 6px 20px rgba(0,0,0,0.08); /* Sombra más pronunciada */
        overflow: hidden;               /* Para que las esquinas redondeadas funcionen */
        margin-bottom: 2rem;
    }

    /* --- (B) Filas internas (las que crea st.container(border=True)) --- */
    .table-container [data-testid="stContainer"][style*="border"] {
        /* ¡RESET! Quitamos todos los estilos de "tarjeta" */
        background-color: transparent;
        box-shadow: none;
        border-radius: 0;
        border: none; /* Quitamos el borde que pone Streamlit */
        margin-bottom: 0;
        padding: 0.5rem 0 !important; /* Ajuste de padding */
        
        /* ¡LÍNEA HORIZONTAL! */
        border-bottom: 1px solid #e0e0e0; /* La línea divisoria horizontal */
    }

    /* --- (C) Fila de Cabecera --- */
    .table-container > [data-testid="stContainer"][style*="border"]:first-of-type {
        background-color: #f0f4f8; /* Fondo gris claro para la cabecera */
        font-weight: 700; /* Más negrita */
        color: #343a40; /* Color de texto más oscuro */
        border-bottom: 2px solid #d0d0d0; /* Línea más gruesa para el header */
        padding: 0.75rem 0 !important; /* Ajuste de padding */
    }

    /* --- (D) Quitar línea horizontal de la última fila --- */
    .table-container > [data-testid="stContainer"][style*="border"]:last-of-type {
        border-bottom: none; /* La última fila no necesita línea abajo */
    }

    /* --- (E) ¡¡LÍNEAS VERTICALES!! (Las celdas) --- */
    .table-container [data-testid="stContainer"][style*="border"] div[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"] {
        /* ¡LÍNEA VERTICAL DIVISORA! */
        border-right: 1px solid #e0e0e0; /* Borde vertical sutil */
        
        /* Padding interno de la celda */
        padding: 0.75rem 0.75rem !important; 

        /* Alineación vertical */
        display: flex;
        align-items: center;
        min-height: 56px; /* Altura mínima de fila aumentada */
    }

    /* Quita la línea vertical de la ÚLTIMA columna (celda) */
    .table-container [data-testid="stContainer"][style*="border"] div[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"]:last-child {
        border-right: none !important;
    }
    
    /* --- (F) Ajustes para widgets (Botones, Selects, Texto) --- */

    /* Ajuste para los selectbox (Status, Certificado) */
    .table-container div[data-testid="stSelectbox"] {
         width: 100% !important;
         min-height: 0 !important;
         height: auto !important;
    }
    .table-container div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
         min-height: 0 !important;
         height: 38px !important; 
         padding-top: 0.2rem !important;
         padding-bottom: 0.2rem !important;
         border-color: #d0d7de !important;
    }
    
    /* Ajuste para el texto simple (st.write) */
    .table-container [data-testid="stMarkdown"] {
        flex: 1;           /* Hace que el contenedor de texto crezca */
        min-width: 0;      /* ¡¡LA MAGIA!! Permite que el texto se encoja y se ajuste */
    }
    .table-container [data-testid="stMarkdown"] p {
        margin: 0;
        padding: 0;
        word-wrap: break-word; /* Fuerza el ajuste de palabra */
        overflow-wrap: break-word; 
        white-space: normal; /* Asegura el ajuste */
    }

    /* ================================================================== */
    /* === 6. ALERTAS Y DIÁLOGOS === */
    /* ================================================================== */
    [data-testid="stAlert"] {
        border-left: 4px solid #f59f00 !important;
        background: #fff7e6 !important;
    }
    [data-testid="stAlert"] button[kind="primary"] {
        background-color: #f59f00 !important;
        color: #2129 !important;
    }
    [data-testid="stAlert"] button[kind="primary"]:hover {
        background-color: #e67700 !important;
        color: #fff !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-thumb {
        background: #b0b7c3;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #8b97a8;
    }

    </style>
    """, unsafe_allow_html=True)

