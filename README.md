# 🎓 Sistema de Gestión de Recibos

Un sistema web completo desarrollado con Streamlit para la gestión de alumnos, grupos, profesores y generación automática de recibos de pago.

## 📋 Características Principales

### 🏠 Dashboard Principal
- Resumen general del sistema con métricas clave
- Contador de alumnos activos
- Ingresos del mes actual
- Grupos activos
- Montos pendientes de pago

### 👥 Gestión de Alumnos
- Registro completo de nuevos alumnos
- Asignación a grupos específicos
- Control de estados (Activo, Baja, Restringido, Finalizado)
- Gestión de certificados
- Búsqueda avanzada por nombre, matrícula o correo
- Filtrado por grupo y estado

### 📚 Gestión de Grupos
- Creación y administración de grupos
- Asignación de profesores
- Control de fechas de inicio y término
- Estados automáticos (Próximo → Activo → Finalizado)
- Historial completo de grupos archivados

### 👨‍🏫 Gestión de Profesores
- Registro de profesores
- Control de estados (Activo/Inactivo)
- Asignación a grupos

### 🧾 Sistema de Recibos
- Registro de pagos por concepto
- Generación automática de PDFs con:
  - Logo de la institución
  - Información de contacto
  - Datos del alumno y pago
  - Conversión de números a letras
  - Firma digital
- Historial completo de pagos
- Búsqueda por folio o nombre

### 📊 Historial y Reportes
- Historial completo de grupos finalizados
- Datos archivados de alumnos por grupo
- Información de profesores y fechas

## 🛠️ Tecnologías Utilizadas

- **Frontend**: Streamlit
- **Base de Datos**: PostgreSQL
- **Generación de PDFs**: FPDF2
- **Procesamiento de Datos**: Pandas, NumPy
- **Conversión de Números**: num2words
- **Procesamiento de Imágenes**: Pillow

## 📦 Instalación

### Prerrequisitos
- Python 3.8 o superior
- PostgreSQL 12 o superior
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd sistema-recibos
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la base de datos**
   - Crear una base de datos PostgreSQL
   - Ejecutar los scripts SQL necesarios para crear las tablas
   - Configurar la cadena de conexión

5. **Configurar variables de entorno**
   - Crear archivo `.streamlit/secrets.toml` con la configuración de la base de datos:
   ```toml
   [DB_CONNECTION_STRING]
   db_connection_string = "postgresql://usuario:contraseña@localhost:5432/nombre_bd"
   ```

6. **Ejecutar la aplicación**
   ```bash
   streamlit run sistemaR.py
   ```

## 📁 Estructura del Proyecto

```
sistema-recibos/
├── pages/
│   ├── administracion.py      # Gestión de alumnos, grupos y profesores
│   ├── Historial.py           # Historial de grupos finalizados
│   └── recibos.py             # Sistema de recibos y pagos
├── utils/
│   ├── css.py                 # Estilos personalizados
│   ├── logo_principal.jpg     # Logo de la institución
│   ├── info_contacto.png      # Barra de información de contacto
│   └── firma.jpg             # Imagen de firma para recibos
├── sistemaR.py               # Aplicación principal (Dashboard)
├── requirements.txt          # Dependencias del proyecto
└── README.md                # Este archivo
```

## 🗄️ Estructura de la Base de Datos

El sistema utiliza las siguientes tablas principales:

- **Alumnos**: Información personal y académica
- **Grupos**: Datos de grupos y fechas
- **Profesores**: Información del personal docente
- **Inscripciones**: Relación alumnos-grupos
- **Pagos**: Registro de pagos y recibos
- **Grupos_Historial**: Archivo de grupos finalizados

## 🎨 Personalización

### Imágenes Personalizadas
Para personalizar el sistema con tu institución:

1. **Logo Principal**: Reemplaza `utils/logo_principal.jpg`
2. **Información de Contacto**: Reemplaza `utils/info_contacto.png`
3. **Firma**: Reemplaza `utils/firma.jpg`

### Estilos CSS
Los estilos se encuentran en `utils/css.py` y pueden ser modificados para cambiar:
- Colores del tema
- Tipografías
- Espaciado y diseño
- Efectos visuales

## 🔧 Configuración Avanzada

### Variables de Entorno
El sistema utiliza Streamlit Secrets para la configuración sensible:

```toml
# .streamlit/secrets.toml
[DB_CONNECTION_STRING]
db_connection_string = "postgresql://usuario:contraseña@host:puerto/base_datos"
```

### Personalización de Conceptos de Pago
Los conceptos de pago están definidos en `pages/recibos.py`:
- Inscripción
- Mensualidad 1-6

Puedes modificar esta lista según tus necesidades.

## 🚀 Uso del Sistema

### Primer Uso
1. Accede al dashboard principal
2. Configura profesores en la pestaña "Profesores"
3. Crea grupos en la pestaña "Grupos"
4. Registra alumnos y asígnalos a grupos
5. Comienza a registrar pagos y generar recibos

### Flujo de Trabajo Típico
1. **Configuración inicial**: Profesores → Grupos → Alumnos
2. **Operación diaria**: Registro de pagos → Generación de recibos
3. **Finalización**: Archivar grupos completados

## 🔒 Seguridad

- Las credenciales de base de datos se almacenan en archivos de configuración locales
- El archivo `.gitignore` excluye información sensible
- Se recomienda usar variables de entorno en producción

## 📝 Notas de Desarrollo

- El sistema está diseñado para ser fácilmente extensible
- Los modales utilizan el decorador `@st.dialog` de Streamlit
- La conexión a base de datos incluye manejo robusto de errores
- Los PDFs se generan dinámicamente con información actualizada

## 🤝 Contribuciones

Para contribuir al proyecto:
1. Fork del repositorio
2. Crear una rama para tu feature
3. Realizar los cambios
4. Enviar un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia de Carpediem México.

## 📞 Soporte

Para soporte técnico o consultas sobre el sistema, contactar a colaboradores.

**Desarrollado con ❤️ para la gestión educativa eficiente, Carpediem Mexico y Oscar Jimenez**
