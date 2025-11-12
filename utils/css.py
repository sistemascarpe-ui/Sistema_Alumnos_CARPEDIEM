import streamlit as st

def load_css():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] [data-testid="stSidebarNavItems"] {
        display: none !important;
    }

    /* Estilo para el botón de colapsar la barra lateral */
    [data-testid="stSidebarCollapseButton"] span svg {
        color: #000000 !important;
    }

    /* ================================================================== */
    /* === 1. CONFIGURACIÓN GENERAL Y MENÚ DOBLE FIX === */
    /* ================================================================== */


    body {
        background-color: #f0f4f8;
        text-align: center !important;
    }
    .stApp {
        background-color: #f0f4f8 !important;
        color: #343a40 !important;
        font-family: 'Segoe UI', Tahoma, sans-serif !important;
        padding: 1.2rem !important;
        max-width: 100% !important;
        margin: 0 auto !important;
    }
    /* Añadir alineación centrada para encabezados h2, h3, h4 globales */
    h1, h2, h3, h4, h5, h6 {
        text-align: center !important;
    }
    /* Esta regla es solo para centrar componentes NATIVOS de Streamlit */
    [data-testid="stTable"], [data-testid="stDataFrame"] {
        margin-left: auto !important;
        margin-right: auto !important;
        display: block !important;
    }

    /* Excluir formularios y sus elementos del centrado global */
    div[data-testid="stForm"], div[data-testid="stForm"] * {
        text-align: left !important;
    }

    /* Alinear a la izquierda todos los elementos dentro de los select box */
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

    /* Reduce width of Grupo and Alumno selectbox containers to 50% (responsive) */
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
        /* ¡¡AÑADE ESTA LÍNEA AQUÍ!! */
        color: #31333F !important;
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
        /* Reducir el ancho de los select box a la mitad */
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
        border: 2px solid #1500FF !important; /* Borde inicial */
        transition: all 0.2s ease !important;
        /* ¡¡AÑADE ESTAS 2 LÍNEAS!! */
        background-color: white !important; 
        color: #1500FF !important;
    }
    button:hover {
        border-color: #FF8400 !important; /* Borde al pasar el cursor */
        /* ¡¡AÑADE ESTAS 2 LÍNEAS!! */
        background-color: #f7f7f7 !important; /* Un fondo ligero al pasar */
        color: #FF8400 !important;
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
    [data-testid="stDataFrame"] {
        width: 100% !important;
        overflow-x: auto !important;
        display: block !important;
        border: 2px solid #0d47a1 !important; /* Borde general más pronunciado */
        border-radius: 10px !important; /* Bordes más redondeados */
        box-shadow: 0 6px 18px rgba(0,0,0,0.15) !important; /* Sombra más visible */
        margin-bottom: 2rem !important;
        text-align: center !important; /* Centrar el contenido general del DataFrame */
    }
    
    /* Estilo para las celdas de la tabla */
    [data-testid="stDataFrame"] table th,
    [data-testid="stDataFrame"] table td {
        border: 1px solid #e0e0e0 !important; /* Bordes para celdas */
        padding: 12px 18px !important; /* Relleno aumentado */
        text-align: center !important; /* Alineación de texto centrada */
        vertical-align: middle !important; /* Alineación vertical centrada */
    }

    /* Estilo para los encabezados de la tabla */
    [data-testid="stDataFrame"] table th {
        background-color: #0d47a1 !important; /* Fondo azul marino */
        color: white !important; /* Texto blanco */
        font-weight: 700 !important; /* Texto más negrita */
        text-transform: uppercase !important; /* Texto en mayúsculas */
        text-align: center !important; /* Centrar texto del encabezado */
    }

    /* Centrar todos los elementos dentro de las celdas de la tabla */
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

    /* Rayado de cebra para filas */
    [data-testid="stDataFrame"] table tbody tr:nth-child(even) {
        background-color: #f8f9fa !important; /* Color para filas pares */
    }

    [data-testid="stDataFrame"] table tbody tr:hover {
        background-color: #e9ecef !important; /* Resaltar fila al pasar el ratón */
        cursor: pointer !important;
    }
    
    /* Ajustar el tamaño de texto en tablas para dispositivos pequeños */
    @media (max-width: 768px) {
        [data-testid="stDataFrame"] table {
            font-size: 0.9rem !important;
        }
        [data-testid="stDataFrame"] th,
        [data-testid="stDataFrame"] td {
            padding: 0.6rem !important;
        }
    }
    
    /* Alineación vertical de contenido en tablas */
    [data-testid="stDataFrame"] table {
        width: 100% !important;
    }
    
    /* Centrar contenido de los encabezados de tabla */
    [data-testid="stDataFrame"] .stMarkdownContainer,
    [data-testid="stDataFrame"] .stVerticalBlock div[data-testid="stMarkdownContainer"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important; /* Asegurar centrado de texto */
    }

    /* Centrar contenido de divs dentro de celdas de tabla */
    [data-testid="stDataFrame"] td > div,
    .tabla-estilizada td > div {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        height: 100% !important;
    }

    /* Estilos para st.dataframe con clase personalizada */
    .styled-dataframe {
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
        overflow: hidden !important; /* Asegura que los bordes redondeados se vean bien */
    }

    .styled-dataframe table {
        width: 100% !important;
        border-collapse: collapse !important;
    }

    .styled-dataframe th {
        background-color: #f8f9fa !important;
        font-weight: bold !important;
        color: #343a40 !important;
        padding: 10px 15px !important;
        text-align: center !important;
        border: 1px solid #e0e0e0 !important;
    }

    .styled-dataframe td {
        padding: 8px 15px !important;
        text-align: center !important;
        border: 1px solid #e0e0e0 !important;
    }

    .styled-dataframe tbody tr:nth-child(even) {
        background-color: #f2f2f2 !important;
    }

    .styled-dataframe tbody tr:hover {
        background-color: #e9ecef !important;
    }

    /* Asegurar que las imágenes no desborden su contenedor */
    img {
        max-width: 100% !important;
        height: auto !important;
    }

    /* Restricted section text fixes */
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
        gap: 10px; /* Espacio entre el input y el botón */
    }

    .st-emotion-cache-1r6slb0 > div > div:has(div[data-testid="stTextInput"]) {
        flex-grow: 1;
    }

    /* Ocultar mensaje 'press enter to submit form' de formularios Streamlit */
    [data-testid="stFormSubmitHint"] {
        display: none !important;
    }

    /* ================================================================== */
    /* === 7. ESTILOS PARA TABLAS HTML (.tabla-estilizada terminada) === */
    /* ================================================================== */

    /* Contenedor general de la tabla generada por .to_html() */
    .tabla-estilizada {
        width: 100%;                  /* Ocupa todo el ancho */
        border-collapse: collapse;    /* Bordes limpios */
        margin: 2rem 0;               /* Margen arriba y abajo */
        font-size: 0.95em;            /* Tamaño de fuente legible */
        font-family: 'Segoe UI', Tahoma, sans-serif; /* Coincide con tu body */
        border-radius: 12px;          /* Coincide con tus .floating-card */
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); /* Coincide con tus expanders */
        overflow: hidden;             /* Importante para que el border-radius se vea */
        border: 1px solid #e5e7eb;    /* Borde sutil */
    }

    /* Encabezados de la tabla (th) */
    .tabla-estilizada thead tr {
        background-color: #0d47a1;    /* Coincide con tu .main-header */
        color: #ffffff;               /* Texto blanco */
        text-align: center;           /* Alineación centrada (como en tu stDataFrame) */
        font-weight: 600;
    }

    /* Celdas del encabezado (th) y celdas de datos (td) */
    .tabla-estilizada th,
    .tabla-estilizada td {
        padding: 12px 15px;           /* Relleno cómodo */
        text-align: center;           /* Alineación centrada */
    }

    /* Celdas del cuerpo (tbody) */
    .tabla-estilizada tbody tr {
        border-bottom: 1px solid #e5e7eb; /* Línea divisoria entre filas */
    }

    /* Estilo "Zebra" - filas pares */
    .tabla-estilizada tbody tr:nth-of-type(even) {
        background-color: #f8f9fa;    /* Gris muy claro */
    }

    /* Última fila con un borde más grueso */
    .tabla-estilizada tbody tr:last-of-type {
        border-bottom: 2px solid #0d47a1; /* Borde final que coincide con el header */
    }

    /* Efecto al pasar el mouse (hover) */
    .tabla-estilizada tbody tr:hover {
        background-color: #e9ecef;    /* Coincide con tu hover de stDataFrame */
        cursor: default;
    }

    /* ================================================================== */
    /* === 8. (ACTUALIZADO) FIX PARA MODO OSCURO DEL NAVEGADOR === */
    /* ================================================================== */
    /* Fuerza los estilos claros incluso si el navegador está en modo oscuro */

    /* Arregla el fondo del Form/Expander */
    html[data-theme="dark"] [data-testid="stExpander"],
    html[data-theme="dark"] [data-testid="stForm"],
    html[data-theme="dark"] .st-emotion-cache-1r6slb0 {
        background-color: white !important;
        border: 1px solid #e5e7eb !important;
    }

    /* Arregla el cabezal del expander (la barra oscura de tu foto) */
    html[data-theme="dark"] [data-testid="stExpander"] > summary {
        background-color: #f0f4f8 !important; /* Fondo gris claro */
        color: #31333F !important; /* Texto oscuro */
    }
    html[data-theme="dark"] [data-testid="stExpander"] > summary:hover {
         background-color: #e5e7eb !important;
    }

    /* Arregla los inputs (los campos de texto) */
    html[data-theme="dark"] div[data-testid="stTextInput"] input,
    html[data-theme="dark"] div[data-testid="stNumberInput"] input,
    html[data-theme="dark"] div[data-testid="stDateInput"] input,
    html[data-theme="dark"] div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: white !important;
        color: #31333F !important;
        border: 1px solid #dfe1e5 !important;
    }

    /* Arregla el color del texto 'placeholder' (ej. "Nombre completo") */
    html[data-theme="dark"] ::-webkit-input-placeholder { color: #a0a0a0 !important; }
    html[data-theme="dark"] ::-moz-placeholder { color: #a0a0a0 !important; }
    html[data-theme="dark"] :-ms-input-placeholder { color: #a0a0a0 !important; }
    html[data-theme="dark"] :-moz-placeholder { color: #a0a0a0 !important; }

    /* ================================================================== */
    /* === 9. (NUEVO) FIX PARA EL BOTÓN DE COLAPSAR SIDEBAR === */
    /* ================================================================== */
    
    /* Apuntamos al 'button' DENTRO del 'div' con el test-id */
    [data-testid="stSidebarCollapseButton"] button {
        background-color: transparent !important;
        border: none !important;
        color: white !important; /* Color del icono (flecha) */
    }

    /* Y lo mismo para el :hover */
    [data-testid="stSidebarCollapseButton"] button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important; /* Un leve brillo blanco */
        border: none !important;
        color: white !important;
    }

    </style>
    """, unsafe_allow_html=True)
