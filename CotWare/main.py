import flet as ft

# Configuración inicial
def main(page: ft.Page):
    page.title = "CotWare"
    page.window_width = 800
    page.window_height = 600
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
        if view_name == "pantalla_1":
            content_area.controls.append(pantalla_1_view())
        elif view_name == "pantalla_2":
            content_area.controls.append(pantalla_2_view())
        else:
            content_area.controls.append(menu_view())
        page.update()

    # Barra lateral de navegación
    nav_rail = ft.NavigationRail(
        selected_index=0,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.HOME, label="Menú"),
            ft.NavigationRailDestination(icon=ft.icons.PAGEVIEW, label="Pantalla 1"),
            ft.NavigationRailDestination(icon=ft.icons.SETTINGS, label="Pantalla 2"),
        ],
        on_change=lambda e: navegar_a(
            ["menu", "pantalla_1", "pantalla_2"][e.control.selected_index]
        ),
    )

    # Área de contenido dinámico
    content_area = ft.Column(expand=True)

    # Pantalla principal (Menú)
    def menu_view():
        return ft.Column(
            controls=[
                ft.Text("Bienvenido a CotWare", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Selecciona una opción desde la barra lateral.", size=18),
                ft.ElevatedButton(
                    "Cambiar Tema", 
                    on_click=toggle_theme,
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.BLUE_GREY_500
                    ),
                ),
            ],
        )

    # Pantalla 1
    def pantalla_1_view():
        return ft.Column(
            controls=[
                ft.Text("Pantalla 1: Aquí puedes agregar funcionalidad específica", size=20),
            ],
        )

    # Pantalla 2
    def pantalla_2_view():
        return ft.Column(
            controls=[
                ft.Text("Pantalla 2: Configuración u otras herramientas", size=20),
            ],
        )

    # Configurar layout principal
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

    # Vista inicial
    content_area.controls.append(menu_view())
    page.update()

# Ejecutar la aplicación
ft.app(target=main)
