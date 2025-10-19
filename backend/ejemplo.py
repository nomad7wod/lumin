import re
from PyPDF2 import PdfReader

# Ruta del PDF
pdf_path = "FichaTransporte.pdf"


# Leer texto del PDF
reader = PdfReader(pdf_path)
pdf_text = ""
for page in reader.pages:
    pdf_text += page.extract_text()

def get_nro_guia(pdf):
    texto = re.search(r"(N°\s*)?EG\d{2}\s*-\s*\d+", pdf)
    return texto.group(0)[3:] if texto else "No encontrado"

def get_punto_partida(pdf):
    texto = re.search(r"inicio de Traslad(?:o)?\s*:\s*(.*?)\s*Punto de ll(?:egada)?", pdf, re.DOTALL)
    if texto:
        partes = re.split(r'Peru -', texto.group(1))
        resultado = partes[-1].strip()
        distrito = resultado.split()[0] if resultado else "Fuera de Peru"
        return distrito
    else:
        return "No encontrado"

def get_observaciones(pdf):
    texto = re.search(r"GUIA:\s*(.*?)\s*placa:", pdf)
    return texto.group(1).strip() if texto else "No encontrado"

def get_conductor(pdf):
    vehiculos_a_conductores = re.search(
        r"Datos de los vehículos\s*:\s*(.*?)\s*Datos de los conductores", pdf, re.DOTALL
    )
    if vehiculos_a_conductores:
        principal_a_guion = re.search(
            r"Principal\s*:\s*(.*?)\s*-", vehiculos_a_conductores.group(1)
        )
        nombre = principal_a_guion.group(1).strip() if principal_a_guion else "No encontrado"
        palabras = nombre.split()
        if len(palabras) >= 2:
            return palabras[-2]  # penúltima palabra (apellido)
        else:
            return nombre
    else:
        return "No encontrado"

# Ejemplos de uso
print("---*" * 10)
print("Ejemplo punto de partida:", get_punto_partida(pdf_text))
print("Ejemplo nro de guia:", get_nro_guia(pdf_text))
print("Ejemplo observaciones:", get_observaciones(pdf_text))
print("Ejemplo conductor:", get_conductor(pdf_text))