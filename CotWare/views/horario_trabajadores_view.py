import flet as ft

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
HORAS = ["09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00", "12:00 - 13:00", "14:00 - 15:00", "15:00 - 16:00", "16:00 - 17:00"]
trabajadores_disponibles = [
    {"rut": "12345678-1", "nombre": "Juan"}, 
    {"rut": "12345678-2", "nombre": "María"}, 
    {"rut": "12345678-3", "nombre": "Carlos"}, 
    {"rut": "12345678-4", "nombre": "Ana"}, 
    {"rut": "12345678-5", "nombre": "Luis"}
]

class HorarioTrabajadoresView:
    def __init__(self, proyecto, regresar_callback):
        self.proyecto = proyecto
        self.regresar_callback = regresar_callback
        self.horarios = self.proyecto.get("horarios", {dia: {hora: "" for hora in HORAS} for dia in DIAS_SEMANA})
        self.trabajadores_disponibles = trabajadores_disponibles
        self.nombre_trabajador = [trabajador["nombre"] for trabajador in self.trabajadores_disponibles]
        self.rut_trabajador = [trabajador["rut"] for trabajador in self.trabajadores_disponibles]
        self.trabajadores_column = ft.Column()

    def get_view(self):
        # Actualizar la vista de trabajadores al cargar la interfaz
        self.actualizar_trabajadores_column()
        horario_table = ft.Column(
            controls=[
                # Encabezado con días de la semana
                ft.Row(
                    controls=[
                        ft.Text("Hora", weight=ft.FontWeight.BOLD, size=20, color=ft.colors.PURPLE_700)
                    ] + [
                        ft.Text(dia, weight=ft.FontWeight.BOLD, size=20, color=ft.colors.PURPLE_700, width=150) for dia in DIAS_SEMANA
                    ],
                    vertical_alignment=ft.VerticalAlignment.CENTER,
                    spacing=20
                ),
                
                # Filas para cada hora del día
                *[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text(hora, size=16, weight=ft.FontWeight.BOLD),
                                width=100,
                                alignment=ft.alignment.center,
                            ),
                            *[
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Text(
                                                f"{self.horarios[dia][hora]}" if self.horarios[dia][hora] else "Disponible", 
                                                size=14, 
                                                color=ft.colors.BLACK if self.horarios[dia][hora] else ft.colors.GREY_600,
                                                weight=ft.FontWeight.BOLD if self.horarios[dia][hora] else ft.FontWeight.NORMAL,
                                            ),
                                            ft.ElevatedButton(
                                                "Asignar" if self.horarios[dia][hora] == "" else "Cambiar",
                                                on_click=lambda e, d=dia, h=hora: self.abrir_dialogo_asignar_trabajador(e, d, h),
                                                bgcolor=ft.colors.GREEN_600 if self.horarios[dia][hora] == "" else ft.colors.YELLOW_700,
                                                color=ft.colors.WHITE,
                                                width=100,
                                                height=35,
                                            ),
                                        ],
                                        alignment=ft.alignment.center,
                                        spacing=5,
                                    ),
                                    padding=10,
                                    border_radius=8,
                                    bgcolor=ft.colors.GREY_100 if self.horarios[dia][hora] == "" else ft.colors.GREY_300,
                                    width=150,
                                    height=100,
                                    alignment=ft.alignment.center,
                                )
                                for dia in DIAS_SEMANA
                            ],
                        ],
                        spacing=15,
                        alignment=ft.MainAxisAlignment.START,
                    )
                    for hora in HORAS
                ],
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        )
        # Botón para regresar a la vista principal de proyectos
        regresar_btn = ft.ElevatedButton(
            "Volver a Proyectos", 
            on_click=lambda _: self.regresar_callback(), 
            bgcolor=ft.colors.PURPLE_700,
            color=ft.colors.WHITE,
            width=200,
            height=40,
        )
        # Botón para recargar la vista del horario
        recargar_btn = ft.ElevatedButton(
            "Refrescar Vista", 
            on_click=lambda e: self.refrescar_vista(),  # Asegúrate de llamar a refrescar_vista
            bgcolor=ft.colors.BLUE_700,
            color=ft.colors.WHITE,
            width=200,
            height=40,
        )
        # Encabezado y contenido principal de la vista del horario
        page = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(f"Horario Semanal del Proyecto {self.proyecto['nombre']}", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
                        horario_table,
                        recargar_btn,
                        regresar_btn,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.VerticalDivider(width=1),
                self.trabajadores_column,
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=30,
        )
        return page

    def refrescar_vista(self):
        # Vuelve a obtener la vista completa del horario
        self.trabajadores_column.controls.clear()  # Limpia la columna de trabajadores
        self.actualizar_trabajadores_column()  # Actualiza la columna de trabajadores
        self.get_view()  # Refresca toda la vista

    def actualizar_trabajadores_column(self):
        # Actualiza la lista de trabajadores disponibles
        self.trabajadores_column.controls = [
            ft.Text("Trabajadores Disponibles", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
            *[
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("nombre:", size=16, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD),
                                ft.Text(trabajador["nombre"], size=16, color=ft.colors.BLACK),    
                                ft.Text("rut:", size=16, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD),
                                ft.Text(trabajador["rut"], size=16, color=ft.colors.BLACK),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    tooltip="Eliminar Trabajador",
                                    on_click=lambda e, trabajador: self.eliminar_trabajador(trabajador),
                                    icon_color=ft.colors.RED_700,
                                ),
                            ],
                        ),           
                    ],
                    alignment=ft.MainAxisAlignment.END,
                    height=50,
                    width=10,
                    scroll=ft.ScrollMode.AUTO,
                    on_scroll_interval=0,
                ) for trabajador in self.trabajadores_disponibles   
            ],
            ft.ElevatedButton("Añadir Trabajador", on_click=self.abrir_dialogo_nuevo_trabajador)
        ]

    def abrir_dialogo_asignar_trabajador(self, event, dia, hora):
        # Crear un cuadro de diálogo para asignar un trabajador
        trabajador_seleccionado = None

        def on_change(e):
            nonlocal trabajador_seleccionado
            trabajador_seleccionado = e.control.value

        dialog = ft.AlertDialog(
            title=ft.Text(f"Asignar Trabajador a {dia} - {hora}"),
            content=ft.Dropdown(
                label="Seleccionar Trabajador",
                options=[ft.dropdown.Option(trabajador) for trabajador in self.nombre_trabajador],
                on_change=on_change,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.cerrar_dialogo(event)),
                ft.TextButton("Guardar", on_click=lambda _: self.guardar_asignacion(event, dia, hora, trabajador_seleccionado)),
            ],
        )
        event.page.dialog = dialog
        event.page.dialog.open = True
        event.page.update()

    def guardar_asignacion(self, event, dia, hora, trabajador_nombre):
        # Encuentra el trabajador por nombre
        trabajador = next((t for t in self.trabajadores_disponibles if t["nombre"] == trabajador_nombre), None)
        if trabajador:
            self.asignar_horario(trabajador, dia, hora)
        self.cerrar_dialogo(event)
        self.refrescar_vista()

    def asignar_horario(self, trabajador, dia, hora):
        # Asigna un horario a un trabajador
        self.horarios[dia][hora] = trabajador["nombre"]
        self.proyecto["horarios"] = self.horarios

    def cerrar_dialogo(self, event):
        event.page.dialog.open = False
        event.page.update()

    def abrir_dialogo_nuevo_trabajador(self, event):
        nombre_trabajador = ft.TextField(label="Nombre del Trabajador")
        rut_trabajador = ft.TextField(label="RUT del Trabajador")
        dialog = ft.AlertDialog(
            title=ft.Text("Añadir Nuevo Trabajador"),
            content=ft.Column(
                [nombre_trabajador, rut_trabajador],
                height=100
                ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.cerrar_dialogo(event)),
                ft.TextButton("Añadir", on_click=lambda e: self.guardar_nuevo_trabajador(e, nombre_trabajador.value, rut_trabajador.value)),
            ],
        )
        event.page.dialog = dialog
        event.page.dialog.open = True
        event.page.update()

    def guardar_nuevo_trabajador(self, event, nombre, rut):
        if not rut or not nombre:
            event.page.snack_bar = ft.SnackBar(ft.Text("No se aceptan campos vacios.", color=ft.colors.RED_700))
            event.page.snack_bar.open = True
            event.page.update()
        elif rut and nombre:
            # Verifica que el RUT no esté registrado
            if rut in self.rut_trabajador:
                return "El RUT ya está registrado"
            else:
                self.rut_trabajador.append(rut)
                self.nombre_trabajador.append(nombre)
                self.trabajadores_disponibles.append({"nombre": nombre, "rut": rut})  # Añadir un nuevo trabajador con un RUT ficticio
                self.actualizar_trabajadores_column()
                self.trabajadores_column.update()
        self.cerrar_dialogo(event)
        self.refrescar_vista()

    def eliminar_trabajador(self, trabajador):
        if trabajador in self.trabajadores_disponibles:
            self.trabajadores_disponibles.remove(trabajador)
            self.actualizar_trabajadores_column()  # Actualiza la vista de trabajadores
            self.trabajadores_column.update()  # Asegúrate de que se actualice la columna de trabajadores