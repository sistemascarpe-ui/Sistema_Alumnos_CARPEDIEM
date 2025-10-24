# 🚀 Guía de Instalación - Streamlit Cloud

## 📋 Pre-requisitos

- ✅ Cuenta en GitHub
- ✅ Tu código ya subido a GitHub
- ✅ Cuenta en Streamlit Cloud (gratis): https://share.streamlit.io

## ⚡ Pasos Rápidos (5 minutos)

### 1. Sube tu código a GitHub

```bash
# Verifica que estés en la rama main
git status

# Si tienes cambios, haz commit
git add .
git commit -m "Preparado para Streamlit Cloud"
git push
```

### 2. Ve a Streamlit Cloud

Abre en tu navegador: **https://share.streamlit.io**

### 3. Inicia Sesión

- Click en **"Sign in"**
- Selecciona **"Sign in with GitHub"**
- Autoriza la conexión

### 4. Crea Nueva App

Click en **"New app"** y completa:

| Campo | Valor |
|------|-------|
| **Repository** | Selecciona tu repositorio |
| **Branch** | `main` |
| **Main file path** | `sistemaR.py` |
| **Python version** | `3.11` |

### 5. Configura Secrets (Variables de Entorno)

Click en **"Advanced settings"** → **"Secrets"**

Pega esto en el cuadro de texto:

```toml
DB_CONNECTION_STRING = "postgresql://neondb_owner:npg_u8xQzp0fXJmg@ep-lingering-hat-ad08sewq-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
```

Click en **"Save"**

### 6. Deploy

Click en **"Deploy"** y espera 2-3 minutos.

## ✅ ¡Listo!

Tu app estará disponible en:
```
https://tu-usuario-app-name.streamlit.app
```

## 🔄 Actualizar tu App

Cada vez que hagas cambios en GitHub:

```bash
git add .
git commit -m "Descripción de cambios"
git push
```

Streamlit Cloud actualizará automáticamente tu app.

## ⚠️ Troubleshooting

### Error: "Cannot connect to database"

Verifica que el secret `DB_CONNECTION_STRING` esté correctamente configurado en Streamlit Cloud.

### Error: "Module not found"

Verifica que `requirements.txt` tenga todas las dependencias necesarias.

### La app no se actualiza

Haz un "Redeploy" manual desde el dashboard de Streamlit Cloud.

## 📞 Necesitas Ayuda?

- Documentación oficial: https://docs.streamlit.io/streamlit-community-cloud
- Forum: https://discuss.streamlit.io

---

¡Tu sistema estará funcionando en minutos! 🎉

