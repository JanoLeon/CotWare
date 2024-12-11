import flet as ft
from Conexion_BD.db_conexion import Conexion_BD

def gestor_de_tareas_view(navegar_a_callback):

    def obtener_proyectos():
        query = "SELECT * FROM proyectos"
        cursor = Conexion_BD.get_cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def buscar_proyecto(id):
        query = "SELECT * FROM proyectos WHERE ID_Proyecto = %s"
        params = (id,)
        cursor = Conexion_BD.get_cursor()
        cursor.execute(query, params)
        resultado = cursor.fetchone()
        if resultado:
            return [resultado]
        return []
    
    def crear_carrusel_proyectos(proyectos, navegar_a_callback):
        return ft.Row(
            controls=[
                ft.Container(
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
                                on_click=lambda e, p=proyecto: mostrar_formulario_edicion(e, p),
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
                ) for proyecto in proyectos
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            scroll=ft.ScrollMode.ALWAYS  # Scroll horizontal para simular un carrusel
        )

    def buscar_y_mostrar_proyecto(event):
        proyecto_id = event.control.value
        resultados = buscar_proyecto(proyecto_id)
        proyectos_carrusel = crear_carrusel_proyectos(resultados, navegar_a_callback)
        content_area.controls.clear()
        content_area.controls.append(
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Gestión de Cotizaciones", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                            proyectos_carrusel,
                            ft.ElevatedButton(
                                "Atrás",
                                on_click=mostrar_todos_los_proyectos,
                                bgcolor=ft.Colors.BLUE_600,
                                color=ft.Colors.WHITE,
                                width=200,
                            ),
                        ],
                        spacing=20,
                    ),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        controls=[
                            ft.Text(
                                "COTWARE", 
                                size=24, 
                                weight=ft.FontWeight.BOLD, 
                                color=ft.Colors.PURPLE_700
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("ID Cotizacion: 1", weight=ft.FontWeight.BOLD),
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Nombre Proyecto: Proyecto 1", weight=ft.FontWeight.BOLD),
                                    ft.Container(width=20),  # Añade un espacio entre los textos
                                    ft.Text("Cliente: Cliente 1", weight=ft.FontWeight.BOLD),
                                ],
                            ),
                            ft.Divider(
                                height=2,
                                thickness=2,
                                color=ft.Colors.GREY_300
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Producto/s", weight=ft.FontWeight.BOLD, color=ft.Colors.YELLOW_900, width=120, text_align=ft.TextAlign.START),
                                    ft.Text("Item/s", weight=ft.FontWeight.BOLD, color=ft.Colors.YELLOW_900, width=120, text_align=ft.TextAlign.START),
                                    ft.Text("Precio Unitario", weight=ft.FontWeight.BOLD, color=ft.Colors.YELLOW_900, width=120, text_align=ft.TextAlign.START),
                                    ft.Text("Precio Total", weight=ft.FontWeight.BOLD, color=ft.Colors.YELLOW_900, width=120, text_align=ft.TextAlign.START),
                                ],
                            ),
                            ft.Divider(
                                height=2,
                                thickness=2,
                                color=ft.Colors.GREY_300
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Producto 1", width=125),
                                    ft.Text("1 Item", width=153),
                                    ft.Text("$1.000", width=110),
                                    ft.Text("$1.000", width=120),
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Producto 2", width=125),
                                    ft.Text("2 Items", width=153),
                                    ft.Text("$2.000", width=110),
                                    ft.Text("$4.000", width=120),
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Producto 3", width=125),
                                    ft.Text("3 Items", width=153),
                                    ft.Text("$3.000", width=110),
                                    ft.Text("$9.000", width=120),
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Producto 4", width=125),
                                    ft.Text("4 Items", width=153),
                                    ft.Text("$4.000", width=110),
                                    ft.Text("$16.000", width=120),
                                ],
                            ),
                            ft.Divider(
                                height=2,
                                thickness=2,
                                color=ft.Colors.GREY_300
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("", width=125),
                                    ft.Text("", width=153),
                                    ft.Text("Subtotal", width=110),
                                    ft.Text("$30.000", width=120)
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("", width=125),
                                    ft.Text("", width=153),
                                    ft.Text("IVA 19%", width=110),
                                    ft.Text("$5.700", width=120)
                                ],
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("", width=125),
                                    ft.Text("", width=153),
                                    ft.Text("Total", width=110),
                                    ft.Text("$35.700", width=120)
                                ],
                            ),
                        ],
                        spacing=20,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=20,
            )
        )
        event.page.update()

    def mostrar_todos_los_proyectos(event=None):
        proyectos = obtener_proyectos()
        proyectos_carrusel = crear_carrusel_proyectos(proyectos, navegar_a_callback)
        content_area.controls.clear()
        content_area.controls.append(
            ft.Column(
                controls=[
                    ft.Text("Gestión de Cotizaciones", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                    ft.TextField(
                        label="Buscar Proyecto por ID",
                        prefix_icon=ft.Icons.SEARCH,
                        on_submit=buscar_y_mostrar_proyecto,
                        width=400
                    ),
                    proyectos_carrusel,
                ],
                spacing=20,
            )
        )
        if event:
            event.page.update()

    def actualizar_proyecto(proyecto_id, nombre, cliente, estado):
        query = "UPDATE proyectos SET Nombre_Proyecto = %s, Cliente_Proyecto = %s, Estado_Proyecto = %s WHERE ID_Proyecto = %s"
        params = (nombre, cliente, estado, proyecto_id)
        cursor = Conexion_BD.get_cursor()
        cursor.execute(query, params)
        Conexion_BD.get_connection().commit()

    def mostrar_formulario_edicion(event, proyecto):
        nombre_field = ft.TextField(label="Nombre del Proyecto", value=proyecto["Nombre_Proyecto"], width=400)
        cliente_field = ft.TextField(label="Cliente del Proyecto", value=proyecto["Cliente_Proyecto"], width=400)
        estado_dropdown = ft.Dropdown(
            label="Estado del Proyecto",
            options=[
                ft.dropdown.Option("Pendiente"),
                ft.dropdown.Option("Aprobado"),
                ft.dropdown.Option("Rechazado"),
            ],
            value=proyecto["Estado_Proyecto"],
            width=400,
        )

        def guardar_cambios(event):
            actualizar_proyecto(proyecto["ID_Proyecto"], nombre_field.value, cliente_field.value, estado_dropdown.value)
            mostrar_todos_los_proyectos(event)

        content_area.controls.clear()
        content_area.controls.append(
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                        ft.Column(
                            controls=[
                                ft.Text(f"Editar Proyecto {proyecto['ID_Proyecto']}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                                nombre_field,
                                cliente_field,
                                estado_dropdown,
                            ],
                        ),
                        ft.Column(
                            controls=[
                                ft.TextField(
                                    label="Archivo asociado",
                                    value=proyecto["Cotizacion_Proyecto"],
                                    read_only=True,
                                    width=400
                                ),
                            ],
                        ),
                        ft.Row(
                            controls=[
                            ft.ElevatedButton(
                                "Guardar Cambios",
                                on_click=guardar_cambios,
                                bgcolor=ft.Colors.GREEN_600,
                                color=ft.Colors.WHITE,
                                width=200,
                            ),
                            ft.ElevatedButton(
                                "Volver atras",
                                on_click=mostrar_todos_los_proyectos,
                                bgcolor=ft.Colors.RED_600,
                                color=ft.Colors.WHITE,
                                width=200,
                            ),
                            ],
                        ),
                        ],
                    ),
                ],
                spacing=20,
            )
        )
        event.page.update() 

    # Obtener los proyectos desde la base de datos
    proyectos = obtener_proyectos()

    # Crear el carrusel de proyectos
    proyectos_carrusel = crear_carrusel_proyectos(proyectos, navegar_a_callback)

    # Definir la vista con el carrusel de proyectos y el campo de búsqueda
    content_area = ft.Column(
        controls=[
            ft.Text("Gestión de Cotizaciones", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
            ft.TextField(
                label="Buscar Proyecto por ID",
                prefix_icon=ft.Icons.SEARCH,
                on_submit=buscar_y_mostrar_proyecto,
                width=400
            ),
            proyectos_carrusel,
        ],
        spacing=20,
    )

    return content_area