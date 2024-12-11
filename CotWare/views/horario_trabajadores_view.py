import flet as ft
from Conexion_BD.db_conexion import Conexion_BD

horarios_actuales = None
trabajadores_column = ft.Column()
trabajadores_disponibles = []

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
HORAS = ["08:00 - 09:00", "10:00 - 11:00", "12:00 - 13:00", "14:00 - 15:00", "16:00 - 17:00"]

def vista_horario():
    def inicializar_vista(proyecto, regresar_callback):
        global proyecto_actual, regresar_callback_actual, horarios_actuales
        if proyecto is None:
            raise ValueError("El proyecto no puede ser None")
        proyecto_actual = proyecto
        regresar_callback_actual = regresar_callback
        horarios_actuales = {dia: {hora: "Disponible" for hora in HORAS} for dia in DIAS_SEMANA}
        cargar_trabajadores()

    def cargar_trabajadores():
        global trabajadores_disponibles
        query = "SELECT Nombre_Empleado, RUT_Empleado FROM datos_empleados"
        cursor = Conexion_BD.get_cursor()
        cursor.execute(query)
        trabajadores_disponibles = cursor.fetchall()

    def actualizar_trabajadores_column():
        trabajadores_column.controls = [
            ft.Text("Trabajadores Disponibles", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
            *[
                ft.Row(
                    controls=[
                        ft.Text("Nombre: ", size=16, color=ft.Colors.BLACK),
                        ft.Text(trabajador["Nombre_Empleado"], size=16, color=ft.Colors.BLACK),
                        ft.Container(width=20),  # Añade un espacio de 20 píxeles
                        ft.Text("RUT: ", size=16, color=ft.Colors.BLACK),
                        ft.Text(trabajador["RUT_Empleado"], size=16, color=ft.Colors.BLACK),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Eliminar Trabajador",
                            on_click=lambda e, t=trabajador: eliminar_trabajador(t),
                            icon_color=ft.Colors.RED_700,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ) for trabajador in trabajadores_disponibles
            ],
            ft.ElevatedButton("Añadir Trabajador", on_click=abrir_dialogo_nuevo_trabajador),
        ]
        trabajadores_column.update()

    def eliminar_trabajador(trabajador):
        # Implementa la lógica para eliminar un trabajador
        pass

    def abrir_dialogo_nuevo_trabajador(event):
        # Implementa la lógica para abrir un diálogo para añadir un nuevo trabajador
        pass

    def crear_vista_horario():
        titulo = ft.Text(f"Horarios para Proyecto A", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700)
        
        encabezado_horarios = ft.Row(
            controls=[
                ft.Text("Horas", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, width=100, text_align=ft.TextAlign.CENTER),
                *[ft.Text(dia, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, width=150, text_align=ft.TextAlign.CENTER) for dia in DIAS_SEMANA]
            ],
            alignment=ft.MainAxisAlignment.START,
        )

        filas_horarios = [
            ft.Row(
                controls=[
                    ft.Text(hora, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, width=100),
                    *[
                        ft.Card(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Disponible", size=16, color=ft.Colors.BLACK),
                                    ft.ElevatedButton("Asignar", on_click=lambda e, d=dia, h=hora: asignar_empleado(d, h))
                                ],
                                spacing=5,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            width=150,
                            height=100,
                        ) for dia in DIAS_SEMANA
                    ]
                ],
                alignment=ft.MainAxisAlignment.START,
            ) for hora in HORAS
        ]

        encabezado_trabajadores = ft.Column(
            controls=[
                ft.Text("Trabajadores Disponibles", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700, text_align=ft.TextAlign.CENTER),
                ft.Row(
                    controls=[
                        ft.Text("Nombre: Monserrat Kerber", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, width=300, text_align=ft.TextAlign.CENTER),
                        ft.Text("RUT: 12.345.678-9", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, width=155, text_align=ft.TextAlign.CENTER),
                        ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED),  # Espacio para el botón de eliminar
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    controls=[
                        ft.Text("Nombre: Manuel Calderon", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, width=300, text_align=ft.TextAlign.CENTER),
                        ft.Text("RUT: 98.765.432-1", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, width=155, text_align=ft.TextAlign.CENTER),
                        ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED),  # Espacio para el botón de eliminar
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    controls=[
                        ft.Text("Nombre: Benjamin Hermosilla", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, width=300, text_align=ft.TextAlign.CENTER),
                        ft.Text("RUT: 65.437.765-9", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, width=155, text_align=ft.TextAlign.CENTER),
                        ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED),  # Espacio para el botón de eliminar
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    controls=[
                        ft.Text("Nombre: Trabajador 1", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, width=300, text_align=ft.TextAlign.CENTER),
                        ft.Text("RUT: XX.XXX.XXX-X", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, width=155, text_align=ft.TextAlign.CENTER),
                        ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED),  # Espacio para el botón de eliminar
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    controls=[
                        ft.Text("Nombre: Trabajador 2", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, width=300, text_align=ft.TextAlign.CENTER),
                        ft.Text("RUT: XX.XXX.XXX-X", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, width=155, text_align=ft.TextAlign.CENTER),
                        ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED),  # Espacio para el botón de eliminar
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            ],
        )

        filas_trabajadores = [
            ft.Row(
                controls=[
                    ft.Text(trabajador["Nombre_Empleado"], size=16, color=ft.Colors.BLACK, width=150),
                    ft.Text(trabajador["RUT_Empleado"], size=16, color=ft.Colors.BLACK, width=150),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        tooltip="Eliminar Trabajador",
                        on_click=lambda e, t=trabajador: eliminar_trabajador(t),
                        icon_color=ft.Colors.RED_700,
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
            ) for trabajador in trabajadores_disponibles
        ]

        tabla_horarios = ft.Column(
            controls=[encabezado_horarios, *filas_horarios],
            spacing=10,
        )

        tabla_trabajadores = ft.Column(
            controls=[encabezado_trabajadores, *filas_trabajadores],
            spacing=10,
        )

        return ft.Column(
            controls=[
                titulo,
                ft.Row(
                    controls=[
                        tabla_horarios,
                        ft.VerticalDivider(width=1),
                        tabla_trabajadores,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=20,
                )
            ],
            spacing=20,
        )

    def asignar_empleado(dia, hora):
        # Implementa la lógica para asignar un empleado
        print(f"Asignar empleado para {dia} a las {hora}")

    def seleccionar_proyecto_para_horario(page, regresar_callback):
        proyectos = obtener_proyectos()
        proyecto_dropdown = ft.Dropdown(
            label="Seleccionar Proyecto para Ver Horario",
            options=[ft.dropdown.Option(proyecto["ID_Proyecto"]) for proyecto in proyectos],
            on_change=lambda e: on_proyecto_seleccionado(e, proyectos, page, regresar_callback),
            width=400
        )
        return ft.Column(
            controls=[
                ft.Text("Seleccionar proyecto", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                proyecto_dropdown,
            ],
            spacing=20,
        )

    def on_proyecto_seleccionado(event, proyectos, page, regresar_callback):
        proyecto_id = event.control.value
        print(f"Proyecto seleccionado ID: {proyecto_id}")
        proyecto = next((p for p in proyectos if p["ID_Proyecto"] == proyecto_id), None)
        cargar_vista_horario(page, proyecto, regresar_callback)

    def cargar_vista_horario(page, proyecto, regresar_callback):
        if proyecto is not None:
            inicializar_vista(proyecto, regresar_callback)
            page.controls.clear()
            page.controls.append(get_view())
            page.update()

    def get_view():
        if horarios_actuales is None:
            raise ValueError("La vista no ha sido inicializada. Llama a 'inicializar_vista' primero.")
        
        actualizar_trabajadores_column()
        horario_table = crear_vista_horario()
        return ft.Column([
            trabajadores_column,
            horario_table,
            ft.ElevatedButton("Regresar", on_click=regresar_callback_actual)
        ])

    def obtener_proyectos():
        query = "SELECT ID_Proyecto, Nombre_Proyecto FROM proyectos"
        cursor = Conexion_BD.get_cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def mostrar_horario(proyecto, regresar_callback):
        page = ft.Page()
        cargar_vista_horario(page, proyecto, regresar_callback)
        return page

    horario_view = ft.Column(
            controls=[
                crear_vista_horario()
            ]
        )
    return horario_view