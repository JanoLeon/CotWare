import flet as ft
from views.menu_principal_view import Menu_view
from views.gestor_de_tareas_view import gestor_de_tareas_view
from views.proyecto_detalle_view import proyecto_detalle_view
from views.horario_trabajadores_view import HorarioTrabajadoresView
from views.subir_documento_view import subir_documento_view

def main(page: ft.Page):
    # Configuración inicial de la página
    page.title = "COTWARE - Gestión Integral de Cotizaciones"
    page.theme_mode = ft.ThemeMode.LIGHT  # Establecer tema por defecto (claro)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.bgcolor = ft.colors.PURPLE_50  # Fondo de color morado claro para toda la página

    # Lista simulada de proyectos - simulando datos de una base de datos
    proyectos = [
        {"id": "001", "nombre": "Proyecto A", "estado": "Pendiente", "cliente": "Cliente A", "trabajadores": []},
        {"id": "002", "nombre": "Proyecto B", "estado": "Aprobado", "cliente": "Cliente B", "trabajadores": []},
        {"id": "003", "nombre": "Proyecto C", "estado": "Rechazado", "cliente": "Cliente C", "trabajadores": []},
        {"id": "004", "nombre": "Proyecto D", "estado": "Pendiente", "cliente": "Cliente D", "trabajadores": []},
    ]

    # Función para cambiar el tema claro/oscuro
    def toggle_theme(_):
        page.theme_mode = (
            ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        page.update()

    # Área de contenido que se actualiza dinámicamente
    content_area = ft.Column(expand=True)

    # Función para actualizar la vista principal
    def actualizar_vista_principal():
        navegar_a("menu")

    # Función para crear un nuevo proyecto
    def crear_nuevo_proyecto(event):
        nuevo_id = f"{len(proyectos) + 1:03}"
        nuevo_nombre = nombre_field.value
        nuevo_estado = estado_dropdown.value
        nuevo_cliente = cliente_field.value

        if nuevo_nombre and nuevo_estado and nuevo_cliente:
            nuevo_proyecto = {
                "id": nuevo_id,
                "nombre": nuevo_nombre,
                "estado": nuevo_estado,
                "cliente": nuevo_cliente,
                "trabajadores": []
            }
            proyectos.append(nuevo_proyecto)

            # Limpiar campos y mostrar notificación de éxito
            nombre_field.value = ""
            estado_dropdown.value = None
            cliente_field.value = ""
            event.page.snack_bar = ft.SnackBar(ft.Text("Nuevo proyecto creado exitosamente!"))
            event.page.snack_bar.open = True
            actualizar_vista_principal()  # Actualizar vista automáticamente
        else:
            # Mostrar advertencia si faltan datos
            event.page.snack_bar = ft.SnackBar(ft.Text("Por favor, completa todos los campos.", color=ft.colors.RED_700))
            event.page.snack_bar.open = True
            event.page.update()

    # Función para cambiar entre vistas (menú, gestión de tareas, detalles del proyecto, horario, subir documento)
    def navegar_a(view_name, proyecto=None):
        content_area.controls.clear()  # Limpiar el área de contenido antes de añadir la nueva vista

        if view_name == "menu":
            # Vista del menú principal con opción para ver proyectos horizontalmente y crear un nuevo proyecto
            proyectos_carrusel = crear_carrusel_proyectos(proyectos)

            # Campos de entrada para crear un nuevo proyecto
            global nombre_field, estado_dropdown, cliente_field
            nombre_field = ft.TextField(label="Nombre del Nuevo Proyecto", width=400)
            estado_dropdown = ft.Dropdown(
                label="Estado del Nuevo Proyecto",
                options=[
                    ft.dropdown.Option("Pendiente"),
                    ft.dropdown.Option("Aprobado"),
                    ft.dropdown.Option("Rechazado"),
                ],
                width=400,
            )
            cliente_field = ft.TextField(label="Nombre del Cliente", width=400)

            # Agregar carrusel de proyectos y sección para crear un nuevo proyecto
            content_area.controls.append(
                ft.Column(
                    controls=[
                        ft.Text("Bienvenido a COTWARE", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
                        ft.Text("Proyectos Recientes", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_800),
                        proyectos_carrusel,
                        ft.Divider(height=20),
                        ft.Text("Crear un Nuevo Proyecto", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_800),
                        nombre_field,
                        estado_dropdown,
                        cliente_field,
                        ft.ElevatedButton(
                            "Crear Proyecto",
                            on_click=crear_nuevo_proyecto,
                            bgcolor=ft.colors.GREEN_600,
                            color=ft.colors.WHITE,
                            width=200,
                        ),
                    ],
                    spacing=20,
                )
            )
        elif view_name == "gestor_de_tareas":
            # Vista del gestor de tareas que muestra también el carrusel de proyectos
            proyectos_carrusel = crear_carrusel_proyectos(proyectos)
            search_field = ft.TextField(
                label="Buscar Proyecto por ID o Nombre",
                prefix_icon=ft.icons.SEARCH,
                on_change=buscar_proyecto,
                width=400
            )
            content_area.controls.append(
                ft.Column(
                    controls=[
                        ft.Text("Gestión de Cotizaciones", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
                        search_field,
                        proyectos_carrusel,
                    ],
                    spacing=20,
                )
            )
        elif view_name == "proyecto_detalle" and proyecto is not None:
            # Vista de detalles del proyecto con opciones para editar y ver el horario
            content_area.controls.append(
                proyecto_detalle_view(
                    proyecto,
                    lambda: navegar_a("menu"),
                    lambda: navegar_a("horario", proyecto),
                    actualizar_vista_principal  # Llamada para actualizar la vista al guardar cambios
                )
            )
        elif view_name == "horario":
            # Vista del horario del proyecto seleccionado
            if proyecto:
                horario_view = HorarioTrabajadoresView(proyecto, lambda: navegar_a("menu")).get_view()
                content_area.controls.append(horario_view)
            else:
                proyecto_dropdown = ft.Dropdown(
                    label="Seleccionar Proyecto para Ver Horario",
                    options=[ft.dropdown.Option(proyecto["id"]) for proyecto in proyectos],
                    on_change=lambda e: navegar_a("horario", next((p for p in proyectos if p["id"] == e.control.value), None)),
                    width=400
                )
                content_area.controls.append(
                    ft.Column(
                        controls=[
                            ft.Text("Ver Horario de los Trabajadores", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
                            proyecto_dropdown,
                        ],
                        spacing=20,
                    )
                )
        elif view_name == "subir_documento":
            # Vista para subir documentos para los proyectos
            content_area.controls.append(subir_documento_view(proyectos, lambda: navegar_a("menu")))

        page.update()

    # Función para buscar proyectos por ID o nombre
    def buscar_proyecto(event):
        query = event.control.value.lower()
        resultados = [p for p in proyectos if query in p["id"].lower() or query in p["nombre"].lower()]
        content_area.controls.clear()
        proyectos_carrusel = crear_carrusel_proyectos(resultados)
        search_field = ft.TextField(
            label="Buscar Proyecto por ID o Nombre",
            prefix_icon=ft.icons.SEARCH,
            on_change=buscar_proyecto,
            width=400
        )
        content_area.controls.append(
            ft.Column(
                controls=[
                    ft.Text("Gestión de Cotizaciones", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
                    search_field,
                    proyectos_carrusel,
                ],
                spacing=20,
            )
        )
        page.update()

    # Función auxiliar para crear el carrusel de proyectos
    def crear_carrusel_proyectos(proyectos):
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(f"ID: {proyecto['id']}", weight=ft.FontWeight.BOLD),
                            ft.Text(f"Nombre: {proyecto['nombre']}"),
                            ft.Text(f"Cliente: {proyecto['cliente']}"),
                            ft.Text(
                                f"Estado: {proyecto['estado']}",
                                weight=ft.FontWeight.BOLD,
                                color=(
                                    ft.colors.YELLOW_900 if proyecto['estado'] == "Pendiente"
                                    else ft.colors.GREEN_600 if proyecto['estado'] == "Aprobado"
                                    else ft.colors.RED_600
                                )
                            ),
                            ft.ElevatedButton(
                                "Ver / Editar",
                                on_click=lambda e, p=proyecto: navegar_a("proyecto_detalle", p),
                                bgcolor=ft.colors.BLUE_600,
                                color=ft.colors.WHITE,
                                width=150,
                            ),
                            ft.ElevatedButton(
                                "Ver Horario",
                                on_click=lambda e, p=proyecto: navegar_a("horario", p),
                                bgcolor=ft.colors.GREEN_600,
                                color=ft.colors.WHITE,
                                width=150,
                            ),
                        ],
                        spacing=5,
                    ),
                    padding=10,
                    border_radius=8,
                    bgcolor=ft.colors.GREY_200,
                    width=250,
                    height=220,
                ) for proyecto in proyectos
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            scroll="always"  # Scroll horizontal para simular un carrusel
        )

    # Configurar la vista inicial
    navegar_a("menu")

    # Barra lateral de navegación para cambiar entre vistas
    nav_rail = ft.NavigationRail(
        selected_index=0,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.HOME, label="Inicio"),
            ft.NavigationRailDestination(icon=ft.icons.ACCOUNT_TREE_SHARP, label="Gestión COT."),
            ft.NavigationRailDestination(icon=ft.icons.UPLOAD_FILE, label="Subir Documento"),
            ft.NavigationRailDestination(icon=ft.icons.SCHEDULE, label="Horarios"),  # Añadido el botón de Horario
        ],
        on_change=lambda e: navegar_a(
            ["menu", "gestor_de_tareas", "subir_documento", "horario"][e.control.selected_index]
        ),
        bgcolor=ft.colors.PURPLE_300,  # Color morado para la barra lateral
    )

    # Agregar el contenido a la página principal
    page.add(
        ft.Row(
            controls=[
                nav_rail,
                ft.VerticalDivider(width=1),
                content_area,
            ],
            expand=True,
        )
    )

    page.update()

# Ejecutar la aplicación
ft.app(target=main)
