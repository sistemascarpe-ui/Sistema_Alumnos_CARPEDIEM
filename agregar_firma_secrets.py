import base64

# Convertir la firma a Base64
ruta_firma = r'utils/firma.jpg'

try:
    with open(ruta_firma, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
    # Leer el archivo secrets.toml actual
    with open('.streamlit/secrets.toml', 'r') as f:
        content = f.read()
    
    # Verificar si ya existe FIRMA_BASE64
    if 'FIRMA_BASE64' not in content:
        # Agregar FIRMA_BASE64 al final
        content += f'\n\n# Firma para recibos (Base64)\nFIRMA_BASE64 = """{encoded_string}"""'
        
        # Guardar el archivo actualizado
        with open('.streamlit/secrets.toml', 'w') as f:
            f.write(content)
        
        print("✅ FIRMA_BASE64 agregada exitosamente a .streamlit/secrets.toml")
    else:
        print("⚠️  FIRMA_BASE64 ya existe en el archivo secrets.toml")
        
except FileNotFoundError:
    print(f"❌ ERROR: No se encontró el archivo {ruta_firma}")
except Exception as e:
    print(f"❌ ERROR: {e}")

