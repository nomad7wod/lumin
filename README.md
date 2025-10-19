# Lumin Consulting - PDF Processor Demo

Aplicación web que automatiza la extracción de datos de PDFs con **detección automática de tipo de documento**.

## 📁 Estructura del Proyecto

```
lumin-pdf-processor/
├── backend/                # Backend Flask
│   ├── app.py             # Servidor Flask principal
│   ├── pdf_processor.py   # Lógica de procesamiento PDF
│   └── requirements.txt   # Dependencias Python
├── frontend/              # Frontend HTML
│   └── index.html        # Página principal
├── static/               # Archivos estáticos
│   ├── css/
│   │   └── style.css    # Estilos personalizados
│   └── js/
│       └── main.js      # JavaScript para upload
└── uploads/             # PDFs subidos (temporal)
```

## 🚀 Instalación y Uso

### 1. Instalar dependencias Python

```bash
cd backend
pip install -r requirements.txt
```

### 2. Ejecutar el servidor Flask

```bash
cd backend
python app.py
```

El servidor iniciará en `http://localhost:5001`

### 3. Abrir la aplicación

Abre tu navegador y ve a: `http://localhost:5001`

## 📋 Características

- ✅ **Detección automática** de tipo de documento (Ficha de Transporte o Factura)
- ✅ Extracción automática de datos de PDFs
- ✅ Interface web moderna y responsive
- ✅ Procesamiento en tiempo real
- ✅ Resultados instantáneos adaptados al tipo de documento
- ✅ Soporte para múltiples formatos de documento

## � Tipos de Documentos Soportados

### 1️⃣ Ficha de Transporte (Transport Guide)

**Datos Extraídos:**
- **Número de Guía**: Identificador EG##-####
- **Punto de Partida**: Distrito de inicio del traslado
- **Observaciones**: Notas de la guía
- **Conductor**: Apellido del conductor principal

### 2️⃣ Factura (Invoice)

**Datos Extraídos:**
- **Nro. Factura**: Número de factura F###-########
- **Cliente**: Nombre completo de la empresa
- **BK (Booking)**: Código de reserva
- **Contenedor**: Número de contenedor
- **Total USD**: Monto total en dólares

## 🔧 Cómo Funciona

1. **Sube un PDF**: Arrastra y suelta o selecciona un archivo PDF
2. **Detección Automática**: El sistema identifica si es una Ficha de Transporte o Factura
3. **Extracción Inteligente**: Aplica patrones regex específicos según el tipo de documento
4. **Resultados Dinámicos**: Muestra solo los campos relevantes para cada tipo

## 💡 Tecnologías

- **Backend**: Flask (Python)
- **Frontend**: HTML, TailwindCSS, JavaScript
- **PDF Processing**: PyPDF2
- **CORS**: Flask-CORS

## 📝 Notas

- Los PDFs se guardan temporalmente en la carpeta `uploads/`
- El servidor acepta PDFs de hasta 16MB
- Solo se procesan archivos .pdf
