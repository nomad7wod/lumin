# Tipos de Documentos Soportados

## 📋 Resumen

El sistema ahora puede procesar automáticamente **dos tipos de documentos**:

---

## 1️⃣ Ficha de Transporte (Transport Guide)

### Datos Extraídos:
- **Número de Guía**: `EG##-######` (ej: EG24-00123)
- **Punto de Partida**: Distrito de inicio
- **Observaciones**: Notas de la guía
- **Conductor**: Apellido del conductor principal

### Patrones de Detección:
- Presencia de "ficha" o "transporte" en el texto
- Patrón de número de guía: `EG\d{2}-\d+`

---

## 2️⃣ Factura (Invoice)

### Datos Extraídos:
- **Nro. Factura**: `F###-########` (ej: F001-00000096)
- **Cliente**: Nombre completo de la empresa (ej: UNITED CARGO COMPANY S.A.C)
- **BK (Booking)**: Código de reserva (ej: 169FA01518)
- **Contenedor**: Número de contenedor (ej: OTPU6756995)
- **Total USD**: Monto total en dólares (ej: USD 1,298.00)

### Patrones de Detección:
- Presencia de "factura" en el texto
- Patrón de número de factura: `F\d{3}-\d+`

---

## 🔄 Funcionamiento

1. **Detección Automática**: El sistema identifica el tipo de documento al procesar el PDF
2. **Extracción Inteligente**: Aplica los patrones regex correspondientes según el tipo
3. **Resultados Dinámicos**: La interfaz muestra solo los campos relevantes para cada tipo

---

## 💡 Ventajas

- ✅ Un solo sistema para múltiples tipos de documentos
- ✅ Detección automática del tipo
- ✅ Fácil agregar nuevos tipos de documentos
- ✅ Interfaz adaptable según el documento

---

## 🔧 Para Agregar Nuevos Tipos de Documentos

1. Agregar método de detección en `_detect_document_type()`
2. Crear métodos de extracción para cada campo
3. Actualizar método `process()` para retornar los datos
4. (Opcional) Actualizar frontend para mostrar los campos
