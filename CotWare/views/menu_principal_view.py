import flet as ft
from Conexion_BD.db_conexion import Conexion_BD

def obtener_proyectos():
    query = "SELECT * FROM proyectos"
    cursor = Conexion_BD.get_cursor()
    cursor.execute(query)
    return cursor.fetchall()

def crear_carrusel_proyectos(proyectos, navegar_a_callback):
    containers = []
    for proyecto in proyectos:
        container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(f"ID: {proyecto['ID_Proyecto']}", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Nombre: {proyecto['Nombre_Proyecto']}"),
                    ft.Text(f"Cliente: {proyecto['Cliente_Proyecto']}"),
                    ft.Text(
                        f"Estado: {proyecto['Estado_Proyecto']}",
                        weight=ft.FontWeight.BOLD,
                        color=(
                            ft.Colors.YELLOW_900 if proyecto['Estado_Proyecto'] == "Pendiente"
                            else ft.Colors.GREEN_600 if proyecto['Estado_Proyecto'] == "Aprobado"
                            else ft.Colors.RED_600
                        )
                    ),
                    ft.ElevatedButton(
                        "Ver / Editar",
                        on_click=lambda e, p=proyecto: navegar_a_callback("gestor_de_tareas_view", p),
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        width=150,
                    ),
                    ft.ElevatedButton(
                        "Ver Horario",
                        on_click=lambda e, p=proyecto: navegar_a_callback("horario", p),
                        bgcolor=ft.Colors.GREEN_600,
                        color=ft.Colors.WHITE,
                        width=150,
                    ),
                ],
                spacing=5,
            ),
            padding=10,
            border_radius=8,
            bgcolor=ft.Colors.GREY_200,
            width=250,
            height=220,
        )
        containers.append(container)
    
    return ft.Row(
        controls=containers,
        alignment=ft.MainAxisAlignment.START,
        spacing=10,
        scroll=ft.ScrollMode.ALWAYS  # Scroll horizontal para simular un carrusel
    )

def formulario_crear_proyecto(page, navegar_a_callback):
    nombre_field = ft.TextField(label="Nombre del Proyecto")
    cliente_field = ft.TextField(label="Cliente del Proyecto")
    estado_dropdown = ft.Dropdown(
        label="Estado del Proyecto",
        options=[
            ft.dropdown.Option("Pendiente"),
            ft.dropdown.Option("Aprobado"),
            ft.dropdown.Option("Rechazado"),
        ],
        width=200,
    )

    def crear_proyecto(event):
        query = "INSERT INTO proyectos (Nombre_Proyecto, Cliente_Proyecto, Estado_Proyecto) VALUES (%s, %s, %s)"
        params = (nombre_field.value, cliente_field.value, estado_dropdown.value)
        cursor = Conexion_BD.get_cursor()
        cursor.execute(query, params)
        Conexion_BD.get_connection().commit()  # Obtener la conexión y llamar a commit
        event.page.snack_bar = ft.SnackBar(ft.Text("Proyecto creado exitosamente!"))
        event.page.snack_bar.open = True

        # Actualizar el carrusel de proyectos
        proyectos = obtener_proyectos()
        proyectos_carrusel = crear_carrusel_proyectos(proyectos, navegar_a_callback)
        page.controls[1].controls[0] = proyectos_carrusel  # Actualizar el carrusel en la vista
        page.update()

    return ft.Column(
        controls=[
            ft.Text("Crear Nuevo Proyecto", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
            nombre_field,
            cliente_field,
            estado_dropdown,
            ft.ElevatedButton(
                "Crear Proyecto",
                on_click=crear_proyecto,
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                width=200,
            ),
        ],
        spacing=20,
    )

def menu_principal_view(page, navegar_a_callback):
    proyectos = obtener_proyectos()
    proyectos_carrusel = crear_carrusel_proyectos(proyectos, navegar_a_callback)
    content_area = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Bienvenido a COTWARE",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.PURPLE_700,
                                text_align=ft.TextAlign.CENTER,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            proyectos_carrusel
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        scroll="always",
                    ),
                    ft.Row(
                        controls=[
                            formulario_crear_proyecto(page, navegar_a_callback)
                        ],
                    ),
                ],
            ),
            ft.Column(
                controls=[
                    ft.Card(
                        ft.Container(
                            ft.Column(
                                [
                                    ft.Image(src="icon.png"),
                                    ft.Divider(),
                                    ft.Row(
                                        [
                                            ft.TextField(
                                                icon=ft.Icons.LABEL_SHARP,
                                                label="Nombre",
                                                value="nombre",
                                                read_only=True,
                                                expand=True,
                                            )
                                        ]
                                    ),
                                    ft.Row(
                                        [
                                            ft.TextField(
                                                icon=ft.Icons.LABEL,
                                                label="Cargo",
                                                value="cargo",
                                                read_only=True,
                                                expand=True,
                                            )
                                        ]
                                    ),
                                ]
                            ),
                            width=400,
                            padding=20
                        )
                    ),
                    ft.ElevatedButton(
                        "Ver Perfil",
                        bgcolor=ft.colors.BLUE_600,
                        color=ft.colors.WHITE,
                        width=400,
                        expand=True,
                        on_click=lambda _: navegar_a_callback("perfil")
                    ),
                ],
                alignment=ft.MainAxisAlignment.START
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND
    )
    return content_area