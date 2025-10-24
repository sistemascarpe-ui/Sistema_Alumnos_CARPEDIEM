# Sistema de Gestión de Recibos 🧾

Sistema completo para la gestión de recibos de pago de alumnos.

## 🚀 Desplegar en Streamlit Cloud

### Pasos Rápidos:

1. **Sube tu código a GitHub**
   ```bash
   git add .
   git commit -m "Preparado para Streamlit Cloud"
   git push
   ```

2. **Ve a**: https://share.streamlit.io

3. **Sign in** con GitHub

4. **Crear Nueva App**:
   - Repository: tu repositorio
   - Branch: `main`
   - Main file: `sistemaR.py`
   - Python: `3.11`

5. **Configurar Secrets**:
   ```toml
   DB_CONNECTION_STRING = "tu_connection_string_aqui"
   ```

6. **Deploy** 🎉

## 📝 Documentación Completa

Lee `INSTALACION.md` para instrucciones detalladas.

## 📁 Estructura del Proyecto

```
sistema-recibos/
├── sistemaR.py              # App principal
├── pages/                   # Páginas de Streamlit
│   ├── administracion.py
│   ├── recibos.py
│   └── Historial.py
├── utils/                   # Utilidades
│   └── css.py
├── requirements.txt         # Dependencias
└── INSTALACION.md          # Guía de instalación
```

## 🔧 Requisitos

- Python 3.11+
- PostgreSQL (Neon, Supabase, etc.)
- Streamlit Cloud (para deployment)

## 📚 Características

- ✅ Gestión de alumnos
- ✅ Generación de recibos de pago
- ✅ Administración de grupos
- ✅ Historial de pagos
- ✅ Sistema de autenticación seguro

## 🔐 Seguridad

- Las credenciales se configuran mediante Streamlit Secrets
- **NUNCA** subas `secrets.toml` a GitHub

## 📄 Licencia

Proyecto privado - Todos los derechos reservados

