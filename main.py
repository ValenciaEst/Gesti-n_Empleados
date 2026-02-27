import flet as ft
from datetime import datetime
from gestion_empleados import GestionEmpleados

class AppNomina:

    def __init__(self, page: ft.Page):
        self.page = page
        self.empleado = GestionEmpleados()
        self._setup_page()
        self._create_components()
        self._build_UI()

    def _setup_page(self):  #configurar titulo, colores y tamaño

        self.page.title="Gestion Empleados"
        self.page.window.width = 450
        self.page.window.height = 600
        self.page.theme_mode = ft.ThemeMode.DARK

    def _create_components(self): # instacia botones y campo
       # Pantalla login
       self.campo_pass  = ft.TextField(label="Contraseña", password=True)
       self.btn_ingresar = ft.ElevatedButton("Ingresar", on_click=self._login)


    # Pantalla registro
       self.campo_id     = ft.TextField(label="Identificación")
       self.campo_nombre = ft.TextField(label="Nombre empleado")
       self.radio_genero = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="M", label="Masculino"),
        ft.Radio(value="F", label="Femenino"),
    ]))
       # on_change va dentro como parámetro separado
       self.dropdown_cargo = ft.Dropdown(
        label="Cargo",
       options=[ft.dropdown.Option(c) for c in GestionEmpleados.CARGOS],
       )
       self.dropdown_cargo.on_change = self._actualizar_valor_dia
       self.campo_valor_dia    = ft.TextField(label="Valor día", disabled=True)
       self.campo_dias         = ft.TextField(label="Días laborados")
       self.btn_guardar        = ft.ElevatedButton("Guardar Registro",  on_click=self._guardar)
       self.btn_calcular       = ft.ElevatedButton("Calcular Nómina",   on_click=self._calcular)
       self.btn_salir          = ft.ElevatedButton("Salir",             on_click=self._confirmar_salir)

    def _build_UI(self):
     self.page.add(
        ft.Column([
            ft.Text("Gestión Empleados", size=24, weight="bold", text_align=ft.TextAlign.CENTER),
            ft.Text("Autor: Esteban Valencia Giraldo", size=24, weight="bold", text_align=ft.TextAlign.CENTER),

            self.campo_pass,
            self.btn_ingresar,
        ], spacing=16)
    )
     
    def _login(self, e):
     if self.campo_pass.value == "4682":
        self.page.clean()
        self.page.add(
            ft.Column([
                ft.Text("Registro de Empleado", size=20, weight="bold"),
                self.campo_id, self.campo_nombre,
                ft.Text("Género:"), self.radio_genero,
                self.dropdown_cargo, self.campo_valor_dia,
                self.campo_dias,
                ft.Row([self.btn_guardar, self.btn_calcular, self.btn_salir]),
            ], spacing=12)
        )
     else:
        self.campo_pass.error_text = "Contraseña incorrecta"
        self.page.update()

    def _actualizar_valor_dia(self, e):
     cargo = self.dropdown_cargo.value
     valor = GestionEmpleados.CARGOS.get(cargo, 0)
     self.campo_valor_dia.value = f"${valor:,}"
     self.page.update()

    def _guardar(self, e):
     self.empleado.identificacion = self.campo_id.value
     self.empleado.nombre         = self.campo_nombre.value
     self.empleado.genero         = self.radio_genero.value
     self.empleado.cargo          = self.dropdown_cargo.value
     self.empleado.dias_laborados = int(self.campo_dias.value or 0)


    def _calcular(self, e):
     self._guardar(e)
     cargo     = self.empleado.cargo
     valor_dia = GestionEmpleados.CARGOS.get(cargo, 0)
     total     = self.empleado.calcular_pago(cargo, valor_dia)
     fecha     = datetime.now().strftime("%d/%m/%Y")

     self.page.clean()
     self.page.add(ft.Column([
        ft.Text(" Reporte de Nómina", size=22, weight="bold"),
        ft.Text(f"Fecha: {fecha}"),
        ft.Text(f"ID: {self.empleado.identificacion}"),
        ft.Text(f"Nombre: {self.empleado.nombre}"),
        ft.Text(f"Género: {self.empleado.genero}"),
        ft.Text(f"Cargo: {cargo}"),
        ft.Text(f"Días laborados: {self.empleado.dias_laborados}"),
        ft.Text(f"Valor día: ${valor_dia:,}"),
        ft.Divider(),
        ft.Text(f"TOTAL A PAGAR: ${total:,}", size=20, weight="bold", color="green"),
    ], spacing=10))
     
    def _confirmar_salir(self, e):
     def cerrar(e):
        self.page.close(dialogo)

     def salir(e):
        self.page.window_close()

     dialogo = ft.AlertDialog(
        modal=True,
        title=ft.Text("¿Salir?"),
        content=ft.Text("¿Deseas cerrar la aplicación?"),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar),
            ft.TextButton("Sí, salir", on_click=salir),
        ],
    )
     self.page.open(dialogo)

# Punto de entrada — Flet requiere una función main
# ─────────────────────────────────────────────────
def main(page: ft.Page):
    AppNomina(page)


ft.app(target=main)