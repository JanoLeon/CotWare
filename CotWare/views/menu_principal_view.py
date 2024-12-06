import flet as ft

def Menu_view(toggle_theme, proyectos_recientes, navegar_a_callback):
    return ft.Column(
        controls=[
            ft.Text("Menú Principal", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
            ft.IconButton(icon=ft.icons.DARK_MODE, on_click=toggle_theme, tooltip="Cambiar tema"),
            ft.Text("Proyectos Recientes:", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(f"ID Proyecto: {proyecto['id']}", weight=ft.FontWeight.BOLD),
                                ft.Text(f"Nombre: {proyecto['nombre']}", size=16),
                                ft.Text(f"Estado: {proyecto['estado']}", size=14),
                                ft.ElevatedButton(
                                    "Visualizar Proyecto",
                                    on_click=lambda e, p=proyecto: navegar_a_callback("proyecto_detalle", p),
                                    bgcolor=ft.colors.GREY_500,
                                    color=ft.colors.WHITE
                                ),
                            ],
                            spacing=5,
                        ),
                        padding=10,
                        border_radius=8,
                        bgcolor=ft.colors.GREY_200,
                        width=250,
                        height=200,
                    ) for proyecto in proyectos_recientes
                ],
                alignment=ft.MainAxisAlignment.START,
                scroll="always"
            ),
        ],
        spacing=10,
    )
