import base64
import streamlit as st

# Este script convierte tu firma a Base64 para guardarla en Streamlit Secrets
ruta_firma = r'utils/firma.jpg'

try:
    with open(ruta_firma, "rb") as image_file:
        # Codificar la imagen a Base64
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        print("\n" + "="*70)
        print("✅ FIRMA CONVERTIDA A BASE64")
        print("="*70)
        print("\n⚠️  COPIA ESTE CÓDIGO Y PÉGALO EN TU ARCHIVO .streamlit/secrets.toml:")
        print("\n" + "-"*70)
        print('FIRMA_BASE64 = """' + encoded_string + '"""')
        print("-"*70)
        print("\n📝 INSTRUCCIONES:")
        print("1. Abre el archivo .streamlit/secrets.toml")
        print("2. Pega la línea FIRMA_BASE64 = ... después de DB_CONNECTION_STRING")
        print("3. Guarda el archivo")
        print("4. Reinicia tu app de Streamlit")
        print("\n" + "="*70)
        
except FileNotFoundError:
    print(f"❌ ERROR: No se encontró el archivo en: {ruta_firma}")
    print("   Asegúrate de que el archivo existe en utils/firma.jpg")
except Exception as e:
    print(f"❌ ERROR: {e}")

