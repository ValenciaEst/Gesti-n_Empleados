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




