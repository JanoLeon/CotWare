import flet as ft

def gestor_de_tareas_view(proyectos, navegar_a_callback):
    def obtener_estado_con_color(estado):
        if estado == "Pendiente":
            return ft.Text("Pendiente", color=ft.colors.YELLOW_900)
        elif estado == "Aprobado":
            return ft.Text("Aprobado", color=ft.colors.GREEN_600)
        elif estado == "Rechazado":
            return ft.Text("Rechazado", color=ft.colors.RED_600)
        return ft.Text(estado, color=ft.colors.GREY)

    return ft.Column(
        controls=[
            ft.Text("Gestor de Tareas - Lista de Proyectos", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
            ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(f"ID: {proyecto['id']}", weight=ft.FontWeight.BOLD),
                                ft.Text(f"Nombre: {proyecto['nombre']}"),
                                ft.Row(
                                    controls=[
                                        ft.Text("Estado: "),
                                        obtener_estado_con_color(proyecto["estado"])
                                    ],
                                ),
                                ft.ElevatedButton(
                                    "Editar Proyecto",
                                    on_click=lambda e, p=proyecto: navegar_a_callback("proyecto_detalle", p)
                                ),
                                ft.ElevatedButton(
                                    "Ver Horario",
                                    on_click=lambda e, p=proyecto: navegar_a_callback("horario", p)
                                ),
                            ],
                            spacing=5,
                        ),
                        padding=10,
                        border_radius=8,
                        bgcolor=ft.colors.GREY_200,
                        width=300,
                        height=220,
                    ) for proyecto in proyectos
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            )
        ],
        spacing=10,
    )
