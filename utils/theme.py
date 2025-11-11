# Este es el contenido de utils/theme.py
import streamlit as st

# Importa tus funciones de CSS
try:
    from utils.css import load_css
    from utils.css_dark import load_dark_mode_css
except ImportError:
    st.error("Error: No se pudieron encontrar los archivos css.py o css_dark.py en la carpeta /utils.")
    st.stop()

def update_theme_callback():
    """
    Se llama cuando el st.toggle cambia.
    Actualiza st.session_state.theme basado en el valor del interruptor.
    """
    if st.session_state.get("theme_toggle", False): # Usamos .get() para seguridad
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"

# --- FUNCIÓN 1 (PARA EL INICIO DE PÁGINA) ---
def apply_theme():
    """
    Llama esta función al INICIO de cada página.
    Inicializa y aplica el CSS (claro u oscuro).
    """
    
    # 1. Inicializar el estado del tema si no existe
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

    # 2. Cargar el archivo CSS correcto basado en el estado
    if st.session_state.theme == "dark":
        load_dark_mode_css()
    else:
        load_css()

# --- FUNCIÓN 2 (PARA LA BARRA LATERAL) ---
def show_theme_toggle():
    """
    Llama esta función DENTRO de st.sidebar
    para mostrar el interruptor.
    """
    # Solo mostrar si está logueado
    if "nombre_completo" in st.session_state:
        st.markdown("---")
        st.toggle(
            "🌙 Modo Oscuro",
            value=(st.session_state.theme == "dark"),
            key="theme_toggle",
            on_change=update_theme_callback,
            help="Activa el modo claro u oscuro para la aplicación."
        )