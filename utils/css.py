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

        .filter-container {
            display: flex;
            align-items: center; /* Centra los items verticalmente */
            gap: 1rem; /* Añade un espacio entre el filtro y la búsqueda */
        }

        div[data-testid="stHorizontalBlock"] {
            align-items: center !important;  /* centra todo en la fila */
        }

        div[data-testid="stSelectbox"] {
            margin-top: -25px !important;  /* súbelo */
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

        /* --- Tablas --- */
        .stDataFrame {
            background-color: #ffffff !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06) !important;
            padding: 0.5rem !important;
        }

        .stDataFrame tr:hover {
            background-color: #e3f2fd !important; /* Azul claro al pasar el mouse */
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
    </style>
    """, unsafe_allow_html=True)
