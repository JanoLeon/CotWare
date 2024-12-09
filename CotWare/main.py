import flet as ft
from screeninfo import get_monitors  # Instalar esta librería: pip install screeninfo
from views.menu_principal_view import Menu_view
from views.gestor_de_tareas_view import gestor_de_tareas_view
from views.proyecto_detalle_view import proyecto_detalle_view
from views.horario_trabajadores_view import HorarioTrabajadoresView
from views.subir_documento_view import subir_documento_view
from views.login_view import vista_login
from views.perfil_view import vista_perfil

def main(page: ft.Page):
    # Configuración inicial de la página
    page.title = "COTWARE - Gestión Integral de Cotizaciones"
    page.theme_mode = ft.ThemeMode.LIGHT  # Establecer tema por defecto (claro)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Ajustar el tamaño de la página
    tamaño_monitor = get_monitors()[0]
    page.window_width = tamaño_monitor.width
    page.window_height = tamaño_monitor.height

    # Estado de autenticación
    is_authenticated = False

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
        if is_authenticated:
            navegar_a("menu")
        else:
            navegar_a("login")

    # Función para manejar el inicio de sesión
    def login_success():
        nonlocal is_authenticated
        is_authenticated = True
        actualizar_vista_principal()  # Cambiar a la vista principal después de iniciar sesión

    # Función para cambiar entre vistas (menú, gestor de tareas, detalles del proyecto, horario, subir documento)
    def navegar_a(view_name):
        content_area.controls.clear()  # Limpiar el área de contenido antes de añadir la nueva vista
        
        if not is_authenticated and view_name != "login":
            # Si no está autenticado, forzar a mostrar la vista de login
            view_name = "login"

        if view_name == "login":
            # Vista de login con botón para iniciar sesión
            content_area.controls.append(vista_login(lambda: login_success(), toggle_theme))    
        elif view_name == "menu":
            # Vista del menú principal
            content_area.controls.append(
                ft.Column(
                    controls=[
                        ft.Text("Bienvenido a COTWARE", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
                    ],
                    spacing=20,
                )
            )
        elif view_name == "gestor_de_tareas":
            # Vista del gestor de tareas
            content_area.controls.append(
                ft.Column(
                    controls=[
                        ft.Text("Gestión de Cotizaciones", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
                    ],
                    spacing=20,
                )
            )
        elif view_name == "horario":
            # Vista del horario
            content_area.controls.append(
                ft.Column(
                    controls=[
                        ft.Text("Ver Horarios", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
                    ],
                    spacing=20,
                )
            )
        elif view_name == "subir_documento":
            # Vista para subir documentos
            content_area.controls.append(subir_documento_view([], lambda: navegar_a("menu")))
        elif view_name == "perfil":
            content_area.controls.clear()
            content_area.controls.append(vista_perfil())
        page.update()

    # Configurar la vista inicial
    navegar_a("login")  # Inicializar la vista de login

    # Barra lateral de navegación para cambiar entre vistas
    nav_rail = ft.NavigationRail(
        selected_index=0,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.HOME, label="Inicio"),
            ft.NavigationRailDestination(icon=ft.icons.ACCOUNT_TREE_SHARP, label="Gestión COT."),
            ft.NavigationRailDestination(icon=ft.icons.UPLOAD_FILE, label="Subir Documento"),
            ft.NavigationRailDestination(icon=ft.icons.SCHEDULE, label="Horarios"), 
            ft.NavigationRailDestination(icon=ft.icons.PERSON, label="Perfil"),
        ],
        on_change=lambda e: navegar_a(
            ["menu", "gestor_de_tareas", "subir_documento", "horario", "perfil"][e.control.selected_index]
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
