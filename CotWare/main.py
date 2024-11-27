import flet as ft
from screeninfo import get_monitors  # Instalar esta librería: pip install screeninfo
from views.menu_principal_view import Menu_view
from views.gestor_de_tareas_view import Gestor_de_tareas_view

# Configuración inicial
def main(page: ft.Page):
    page.title = "COTWARE"

    # Obtener resolución de la pantalla principal
    monitor = get_monitors()[0]  # Usamos el monitor principal
    screen_width = monitor.width
    screen_height = monitor.height

    # Calcular tamaño de la ventana proporcionalmente
    window_width = int(screen_width * 0.8)  # 80% del ancho de la pantalla
    window_height = int(screen_height * 0.7)  # 70% de la altura de la pantalla

    # Establecer el tamaño de la ventana
    page.window_width = window_width
    page.window_height = window_height

    # Calcular posición para centrar la ventana
    page.window_left = (screen_width - window_width) // 2
    page.window_top = (screen_height - window_height) // 2

    # Configurar tema inicial
    page.theme_mode = ft.ThemeMode.LIGHT

    # Función para alternar el tema
    def toggle_theme(_):
        page.theme_mode = (
            ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        page.update()

    # Función para cambiar la vista
    def navegar_a(view_name):
        content_area.controls.clear()
        if view_name == "menu":
            content_area.controls.append(Menu_view(toggle_theme))
        elif view_name == "Gestor de tareas":
            content_area.controls.append(Gestor_de_tareas_view(page))

        page.update()

    # Barra lateral de navegación
    nav_rail = ft.NavigationRail(
        selected_index=0,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.HOME, label="Menú"),
            ft.NavigationRailDestination(icon=ft.icons.ACCOUNT_TREE_SHARP, label="Gestor de tareas"),
            #ft.NavigationRailDestination(icon=ft.icons.SETTINGS, label="Pantalla 2"),
        ],
        on_change=lambda e: navegar_a(
            ["menu", "Gestor de tareas", "pantalla_2"][e.control.selected_index]
        ),
    )

    # Área de contenido dinámico
    content_area = ft.Column(expand=True)

    # Configurar layout principal
    content_area.controls.append(Menu_view(toggle_theme))

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
