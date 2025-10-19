import re
from PyPDF2 import PdfReader

class PDFProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pdf_text = self._extract_text()
        self.doc_type = self._detect_document_type()
    
    def _extract_text(self):
        """Extract all text from PDF"""
        reader = PdfReader(self.pdf_path)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text()
        return pdf_text
    
    def _detect_document_type(self):
        """Detect if document is FichaTransporte or Factura"""
        text_lower = self.pdf_text.lower()
        
        # Check for invoice indicators
        if 'factura' in text_lower or re.search(r'f\d{3}-\d+', text_lower):
            return 'FACTURA'
        # Check for transport guide indicators
        elif 'ficha' in text_lower or 'transporte' in text_lower or re.search(r'eg\d{2}\s*-\s*\d+', text_lower):
            return 'FICHA_TRANSPORTE'
        else:
            return 'UNKNOWN'
    
    def get_nro_guia(self):
        texto = re.search(r"(N°\s*)?EG\d{2}\s*-\s*\d+", self.pdf_text)
        return texto.group(0)[3:] if texto else "No encontrado"

    def get_punto_partida(self):
        texto = re.search(r"inicio de Traslad(?:o)?\s*:\s*(.*?)\s*Punto de ll(?:egada)?", self.pdf_text, re.DOTALL)
        if texto:
            partes = re.split(r'Peru -', texto.group(1))
            resultado = partes[-1].strip()
            distrito = resultado.split()[0] if resultado else "Fuera de Peru"
            return distrito
        else:
            return "No encontrado"

    def get_observaciones(self):
        texto = re.search(r"GUIA:\s*(.*?)\s*placa:", self.pdf_text)
        return texto.group(1).strip() if texto else "No encontrado"

    def get_conductor(self):
        vehiculos_a_conductores = re.search(
            r"Datos de los vehículos\s*:\s*(.*?)\s*Datos de los conductores", self.pdf_text, re.DOTALL
        )
        if vehiculos_a_conductores:
            principal_a_guion = re.search(
                r"Principal\s*:\s*(.*?)\s*-", vehiculos_a_conductores.group(1)
            )
            nombre = principal_a_guion.group(1).strip() if principal_a_guion else "No encontrado"
            palabras = nombre.split()
            if len(palabras) >= 2:
                return palabras[-2]
            else:
                return nombre
        else:
            return "No encontrado"
    
    # ============ FACTURA METHODS ============
    
    def get_nro_factura(self):
        """Extract invoice number (e.g., F001-00000096)"""
        texto = re.search(r'(Nro\.?\s*)?F\d{3}-\d+', self.pdf_text, re.IGNORECASE)
        if texto:
            # Extract just the F###-####### part
            factura = re.search(r'F\d{3}-\d+', texto.group(0))
            return factura.group(0) if factura else "No encontrado"
        return "No encontrado"
    
    def get_cliente(self):
        """Extract client name"""
        # Debug: print a snippet of the PDF text to understand the format
        print("🔍 PDF Text snippet (first 500 chars):")
        print(self.pdf_text[:500])
        print("\n🔍 Searching for 'Cliente' or company name patterns...")
        
        # Try different patterns for client
        patterns = [
            # Pattern 1: After "Cliente:" and before "RUC" or line break, then look for company on next line
            r'Cliente:\s*[^\n]*\s*[^\n]*\s*Ciudad:\s*([A-Z][A-Z\s&\.]+(?:S\.A\.C\.|S\.A\.|E\.I\.R\.L\.|S\.R\.L\.))',
            # Pattern 2: Direct match with "Ciudad:" prefix
            r'Ciudad:\s*([A-Z][A-Z\s&\.]+(?:S\.A\.C\.|S\.A\.|E\.I\.R\.L\.|S\.R\.L\.))',
            # Pattern 3: Look for company name near Cliente
            r'Cliente:[\s\S]{0,100}?([A-Z][A-Z\s&\.]{10,}(?:S\.A\.C\.|S\.A\.|E\.I\.R\.L\.|S\.R\.L\.))',
            # Pattern 4: Señor/Señores
            r'Señor(?:es)?\s*:?\s*([A-Z][A-Z\s&\.]+(?:S\.A\.C\.|S\.A\.|E\.I\.R\.L\.|S\.R\.L\.))',
            # Pattern 5: Just match company name with legal entity (last resort)
            r'([A-Z][A-Z\s&\.]{15,}(?:S\.A\.C\.|S\.A\.|E\.I\.R\.L\.|S\.R\.L\.))',
        ]
        
        for i, pattern in enumerate(patterns):
            texto = re.search(pattern, self.pdf_text, re.IGNORECASE | re.MULTILINE)
            if texto:
                cliente = texto.group(1).strip()
                # Clean up extra spaces and newlines
                cliente = re.sub(r'\s+', ' ', cliente)
                print(f"✅ Pattern {i+1} matched: '{cliente}'")
                # Make sure it's a reasonable length and contains company indicators
                if len(cliente) > 10 and ('S.A.C' in cliente.upper() or 'S.A.' in cliente or 'S.R.L' in cliente.upper() or 'E.I.R.L' in cliente.upper()):
                    return cliente
        
        print("❌ No cliente pattern matched")
        return "No encontrado"
    
    def get_booking(self):
        """Extract BK/Booking number (e.g., 169FA01518)"""
        patterns = [
            r'BK\s*:?\s*([A-Z0-9]+)',
            r'Booking\s*:?\s*([A-Z0-9]+)',
            r'B/?K\s*:?\s*([A-Z0-9]+)'
        ]
        
        for pattern in patterns:
            texto = re.search(pattern, self.pdf_text, re.IGNORECASE)
            if texto:
                return texto.group(1).strip()
        
        return "No encontrado"
    
    def get_contenedor(self):
        """Extract container number (e.g., OTPU6756995)"""
        patterns = [
            r'CONTENEDOR\s*:?\s*([A-Z]{4}\d{7})',
            r'Container\s*:?\s*([A-Z]{4}\d{7})',
            r'CNT[RN]\s*:?\s*([A-Z]{4}\d{7})',
            r'\b([A-Z]{4}\d{7})\b'  # Generic container format: 4 letters + 7 digits
        ]
        
        for pattern in patterns:
            texto = re.search(pattern, self.pdf_text, re.IGNORECASE)
            if texto:
                return texto.group(1).strip()
        
        return "No encontrado"
    
    def get_total_usd(self):
        """Extract total amount in USD (e.g., USD 1,298.00)"""
        patterns = [
            r'TOTAL\s+USD\s+([\d,]+\.?\d*)',
            r'Total\s+USD\s+([\d,]+\.?\d*)',
            r'USD\s+([\d,]+\.?\d*)\s*$',
            r'US\$\s*([\d,]+\.?\d*)'
        ]
        
        for pattern in patterns:
            texto = re.search(pattern, self.pdf_text, re.IGNORECASE | re.MULTILINE)
            if texto:
                amount = texto.group(1).strip()
                return f"USD {amount}"
        
        return "No encontrado"
    
    def process(self):
        """Process PDF and return all extracted data based on document type"""
        if self.doc_type == 'FACTURA':
            return {
                "tipo_documento": "Factura",
                "nro_factura": self.get_nro_factura(),
                "cliente": self.get_cliente(),
                "booking": self.get_booking(),
                "contenedor": self.get_contenedor(),
                "total": self.get_total_usd()
            }
        elif self.doc_type == 'FICHA_TRANSPORTE':
            return {
                "tipo_documento": "Ficha de Transporte",
                "nro_guia": self.get_nro_guia(),
                "punto_partida": self.get_punto_partida(),
                "observaciones": self.get_observaciones(),
                "conductor": self.get_conductor()
            }
        else:
            return {
                "tipo_documento": "Desconocido",
                "error": "No se pudo identificar el tipo de documento"
            }
