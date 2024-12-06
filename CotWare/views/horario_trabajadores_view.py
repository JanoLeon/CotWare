import flet as ft

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
HORAS = ["09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00", "12:00 - 13:00", "14:00 - 15:00", "15:00 - 16:00", "16:00 - 17:00"]
trabajadores_disponibles = ["Juan", "María", "Carlos", "Ana", "Luis"]

class HorarioTrabajadoresView:
    def __init__(self, proyecto, regresar_callback):
        self.proyecto = proyecto
        self.regresar_callback = regresar_callback
        self.horarios = self.proyecto.get("horarios", {dia: {hora: "" for hora in HORAS} for dia in DIAS_SEMANA})
        self.trabajadores_disponibles = trabajadores_disponibles
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
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
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
            on_click=lambda _: self.refrescar_vista(),  # Asegúrate de llamar a refrescar_vista
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
                    spacing=20,
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
        self.get_view()  # Llama a get_view para refrescar toda la vista

    def actualizar_trabajadores_column(self):
        # Actualiza la lista de trabajadores disponibles
        self.trabajadores_column.controls = [
            ft.Text("Trabajadores Disponibles", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
            *[
                ft.Row(
                    controls=[
                        ft.Text(trabajador, size=16, color=ft.colors.BLACK),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            tooltip="Eliminar Trabajador",
                            on_click=lambda e, t=trabajador: self.eliminar_trabajador(t),
                            icon_color=ft.colors.RED_700,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ) for trabajador in self.trabajadores_disponibles
            ],
            ft.TextButton("Añadir Trabajador", on_click=self.abrir_dialogo_nuevo_trabajador),
        ]

    def abrir_dialogo_asignar_trabajador(self, event, dia, hora):
        # Crear un cuadro de diálogo para asignar un trabajador
        dialog = ft.AlertDialog(
            title=ft.Text(f"Asignar Trabajador a {dia} - {hora}"),
            content=ft.Dropdown(
                label="Seleccionar Trabajador",
                options=[ft.dropdown.Option(trabajador) for trabajador in self.trabajadores_disponibles],
                on_change=lambda e: self.actualizar_horario(event.page, dia, hora, e.control.value),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.cerrar_dialogo(event)),
                ft.TextButton("Guardar", on_click=lambda _: self.cerrar_dialogo(event)),
            ],
        )
        event.page.dialog = dialog
        event.page.dialog.open = True
        event.page.update()

    def cerrar_dialogo(self, event):
        event.page.dialog.open = False
        event.page.update()

    # Versión corregida
    # Versión corregida
    def actualizar_horario(self, page, dia, hora, trabajador):
        if trabajador:
            self.horarios[dia][hora] = trabajador
        else:
            self.horarios[dia][hora] = ""
        self.proyecto["horarios"] = self.horarios
        self.refrescar_vista()
        page.update()

    def abrir_dialogo_nuevo_trabajador(self, event):
        textfield = ft.TextField(label="Nombre del Trabajador")
        dialog = ft.AlertDialog(
            title=ft.Text("Añadir Nuevo Trabajador"),
            content=textfield,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.cerrar_dialogo(event)),
                ft.TextButton("Añadir", on_click=lambda e: self.guardar_nuevo_trabajador(e)),
            ],
        )
        event.page.dialog = dialog
        event.page.dialog.open = True
        event.page.update()

    def guardar_nuevo_trabajador(self, event):
        # Obtener el TextField del diálogo
        textfield = event.page.dialog.content
        trabajador = textfield.value
        
        if trabajador:
            self.trabajadores_disponibles.append(trabajador)
            self.actualizar_trabajadores_column()
            self.trabajadores_column.update()
        self.cerrar_dialogo(event)

    def eliminar_trabajador(self, trabajador):
        if trabajador in self.trabajadores_disponibles:
            self.trabajadores_disponibles.remove(trabajador)
            self.actualizar_trabajadores_column()  # Actualiza la vista de trabajadores
            self.trabajadores_column.update()  # Asegúrate de que se actualice la columna de trabajadores