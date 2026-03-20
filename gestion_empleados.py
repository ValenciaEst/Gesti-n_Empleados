class GestionEmpleados:

    # Diccionario de cargos con su valor por día
    # La UI lo consulta para llenar el Dropdown y el campo valor_dia
    CARGOS = {
        "Servicios Generales": 40_000,
        "Administrativo":       50_000,
        "Electricista":    60_000,
        "Mecánico":        80_000,
        "Soldador":      90_000,
    }

    def __init__(self, identificacion: str = "", nombre: str = "", genero: str = "", cargo: str = "", dias_laborados: int = 0):
        # Datos personales del empleado
        self.identificacion  = identificacion
        self.nombre          = nombre
        self.genero          = genero

        # Datos laborales
        self.cargo           = cargo
        self.dias_laborados  = dias_laborados

    def calcular_pago(self, cargo: str, valor_dia: int) -> int:
        """Retorna el total a pagar: días laborados × valor del día."""
        return self.dias_laborados * valor_dia

    @staticmethod
    def generar_reporte_pdf(ruta_archivo: str, lineas: list[str]) -> None:
        """Genera un PDF simple usando solo librerías estándar."""
        contenido = [
            "BT",
            "/F1 12 Tf",
            "50 780 Td",
        ]

        for indice, linea in enumerate(lineas):
            texto_limpio = (
                linea.replace("\\", "\\\\")
                .replace("(", "\\(")
                .replace(")", "\\)")
            )
            if indice == 0:
                contenido.append(f"({texto_limpio}) Tj")
            else:
                contenido.append(f"0 -20 Td ({texto_limpio}) Tj")
        contenido.append("ET")
        stream_texto = "\n".join(contenido)
        stream_bytes = stream_texto.encode("latin-1", errors="replace")

        objetos = []
        objetos.append(b"<< /Type /Catalog /Pages 2 0 R >>")
        objetos.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
        objetos.append(
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
            b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
        )
        objetos.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        objetos.append(
            f"<< /Length {len(stream_bytes)} >>\nstream\n".encode("latin-1")
            + stream_bytes
            + b"\nendstream"
        )

        archivo = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]

        for numero_objeto, objeto in enumerate(objetos, start=1):
            offsets.append(len(archivo))
            archivo.extend(f"{numero_objeto} 0 obj\n".encode("latin-1"))
            archivo.extend(objeto)
            archivo.extend(b"\nendobj\n")

        inicio_xref = len(archivo)
        archivo.extend(f"xref\n0 {len(offsets)}\n".encode("latin-1"))
        archivo.extend(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            archivo.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))

        trailer = (
            f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\n"
            f"startxref\n{inicio_xref}\n%%EOF\n"
        )
        archivo.extend(trailer.encode("latin-1"))

        with open(ruta_archivo, "wb") as salida:
            salida.write(archivo)



