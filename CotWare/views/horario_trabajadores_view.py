import flet as ft
from Conexion_BD.db_conexion import Conexion_BD

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
HORAS = ["09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00", "12:00 - 13:00", "14:00 - 15:00", "15:00 - 16:00", "16:00 - 17:00"]
trabajadores_disponibles = [
    {"rut": "12345678-1", "nombre": "Juan"},
    {"rut": "12345678-2", "nombre": "María"},
    {"rut": "12345678-3", "nombre": "Carlos"},
    {"rut": "12345678-4", "nombre": "Ana"},
    {"rut": "12345678-5", "nombre": "Luis"}
]

# Variables globales para mantener el estado
proyecto_actual = None
regresar_callback_actual = None
horarios_actuales = None
trabajadores_column = ft.Column()

def inicializar_vista(proyecto, regresar_callback):
    global proyecto_actual, regresar_callback_actual, horarios_actuales
    if proyecto is None:
        raise ValueError("El proyecto no puede ser None")
    proyecto_actual = proyecto
    regresar_callback_actual = regresar_callback
    horarios_actuales = proyecto.get("horarios", {dia: {hora: "" for hora in HORAS} for dia in DIAS_SEMANA})

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

def abrir_dialogo_nuevo_trabajador(event):
    nombre_trabajador = ft.TextField(label="Nombre del Trabajador")
    rut_trabajador = ft.TextField(label="RUT del Trabajador")
    dialog = ft.AlertDialog(
        title=ft.Text("Añadir Nuevo Trabajador"),
        content=ft.Column([nombre_trabajador, rut_trabajador]),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda _: cerrar_dialogo(event)),
            ft.TextButton("Añadir", on_click=lambda e: guardar_nuevo_trabajador(e, nombre_trabajador.value, rut_trabajador.value)),
        ],
    )
    event.page.dialog = dialog
    event.page.dialog.open = True
    event.page.update()

def guardar_nuevo_trabajador(event, nombre, rut):
    if not nombre or not rut:
        event.page.snack_bar = ft.SnackBar(ft.Text("No se aceptan campos vacíos.", color=ft.Colors.RED_700))
        event.page.snack_bar.open = True
        event.page.update()
    elif rut and nombre:
        if rut in [trabajador["rut"] for trabajador in trabajadores_disponibles]:
            event.page.snack_bar = ft.SnackBar(ft.Text("El RUT ya está registrado.", color=ft.Colors.RED_700))
            event.page.snack_bar.open = True
            event.page.update()
        else:
            trabajadores_disponibles.append({"Nombre_Empleado": nombre, "Rut_Empleado": rut})
            actualizar_trabajadores_column()
            trabajadores_column.update()
    cerrar_dialogo(event)
    refrescar_vista()

def cerrar_dialogo(event):
    event.page.dialog.open = False
    event.page.update()

def eliminar_trabajador(trabajador):
    if trabajador in trabajadores_disponibles:
        trabajadores_disponibles.remove(trabajador)
        actualizar_trabajadores_column()
        trabajadores_column.update()

def abrir_dialogo_asignar_trabajador(event, dia, hora):
    trabajador_seleccionado = None

    def on_change(e):
        nonlocal trabajador_seleccionado
        trabajador_seleccionado = e.control.value

    dialog = ft.AlertDialog(
        title=ft.Text(f"Asignar Trabajador a {dia} - {hora}"),
        content=ft.Dropdown(
            label="Seleccionar Trabajador",
            options=[ft.dropdown.Option(trabajador["Nombre_Empleado"]) for trabajador in trabajadores_disponibles],
            on_change=on_change,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda _: cerrar_dialogo(event)),
            ft.TextButton("Guardar", on_click=lambda _: guardar_asignacion(event, dia, hora, trabajador_seleccionado)),
        ],
    )
    event.page.dialog = dialog
    event.page.dialog.open = True
    event.page.update()

def guardar_asignacion(event, dia, hora, trabajador_nombre):
    trabajador = next((t for t in trabajadores_disponibles if t["Nombre_Empleado"] == trabajador_nombre), None)
    if trabajador:
        asignar_horario(trabajador, dia, hora)
    cerrar_dialogo(event)
    refrescar_vista()

def asignar_horario(trabajador, dia, hora):
    horarios_actuales[dia][hora] = trabajador["Nombre_Empleado"]
    proyecto_actual["horarios"] = horarios_actuales

def refrescar_vista():
    trabajadores_column.controls.clear()
    actualizar_trabajadores_column()
    get_view()

def obtener_proyectos():
    query = "SELECT * FROM proyectos"
    cursor = Conexion_BD.get_cursor()
    cursor.execute(query)
    return cursor.fetchall()

def mostrar_horario(proyecto, regresar_callback):
    inicializar_vista(proyecto, regresar_callback)
    return get_view()

def seleccionar_proyecto_para_horario(page, regresar_callback):
    proyectos = obtener_proyectos()
    proyecto_dropdown = ft.Dropdown(
        label="Seleccionar Proyecto para Ver Horario",
        options=[ft.dropdown.Option(proyecto["ID_Proyecto"]) for proyecto in proyectos],
        on_change=lambda e: cargar_vista_horario(page, next((p for p in proyectos if p["ID_Proyecto"] == e.control.value), None), regresar_callback),
        width=400
    )
    return ft.Column(
        controls=[
            ft.Text("Seleccionar proyecto", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
            proyecto_dropdown,
        ],
        spacing=20,
    )

def cargar_vista_horario(page, proyecto, regresar_callback):
    if proyecto is not None:
        print(proyecto)
        inicializar_vista(proyecto, regresar_callback)
        page.controls.clear()
        page.controls.append(get_view())
        page.update()

def get_view():
    if horarios_actuales is None:
        raise ValueError("La vista no ha sido inicializada. Llama a 'inicializar_vista' primero.")
    
    actualizar_trabajadores_column()
    horario_table = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("Hora", weight=ft.FontWeight.BOLD, size=20, color=ft.Colors.PURPLE_700)
                ] + [
                    ft.Text(dia, weight=ft.FontWeight.BOLD, size=20, color=ft.Colors.PURPLE_700, width=150) for dia in DIAS_SEMANA
                ],
                vertical_alignment=ft.VerticalAlignment.CENTER,
                spacing=20
            ),
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
                                            f"{horarios_actuales[dia][hora]}" if horarios_actuales[dia][hora] else "Disponible",
                                            size=14,
                                            color=ft.Colors.BLACK if horarios_actuales[dia][hora] else ft.Colors.GREY_600,
                                            weight=ft.FontWeight.BOLD if horarios_actuales[dia][hora] else ft.FontWeight.NORMAL,
                                        ),
                                        ft.ElevatedButton(
                                            "Asignar" if horarios_actuales[dia][hora] == "" else "Cambiar",
                                            on_click=lambda e, d=dia, h=hora: abrir_dialogo_asignar_trabajador(e, d, h),
                                            bgcolor=ft.Colors.GREEN_600 if horarios_actuales[dia][hora] == "" else ft.Colors.YELLOW_700,
                                            color=ft.Colors.WHITE,
                                            width=100,
                                            height=35,
                                        ),
                                    ],
                                    alignment=ft.alignment.center,
                                    spacing=5,
                                ),
                                padding=10,
                                border_radius=8,
                                bgcolor=ft.Colors.GREY_100 if horarios_actuales[dia][hora] == "" else ft.Colors.GREY_300,
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

    regresar_btn = ft.ElevatedButton(
        "Volver a Proyectos",
        on_click=lambda _: regresar_callback_actual(),
        bgcolor=ft.Colors.PURPLE_700,
        color=ft.Colors.WHITE,
        width=200,
        height=40,
    )

    recargar_btn = ft.ElevatedButton(
        "Refrescar Vista",
        on_click=lambda e: refrescar_vista(),
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
        width=200,
        height=40,
    )

    page = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Text(f"Horario Semanal del Proyecto {proyecto_actual['Nombre_Proyecto']}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                    horario_table,
                    recargar_btn,
                    regresar_btn,
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.VerticalDivider(width=1),
            trabajadores_column,
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=30,
    )
    return page

