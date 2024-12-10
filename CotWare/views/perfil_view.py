import flet as ft
from Conexion_BD.db_conexion import Conexion_BD

def vista_perfil():
    return ft.Container(
        ft.Row(
            controls=[
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
                                                    expand=True
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
                                                    expand=True
                                                )
                                            ]
                                        ),
                                    ]
                                ),
                                width=400,
                                padding=10,
                            )
                        ),
                    ],
                ),
                ft.Container(
                    ft.Column(
                        controls=[
                            ft.TextField(
                                label="Número de teléfono",
                                value="123456789",
                                read_only=True
                            ),
                            ft.TextField(
                                label="Correo electrónico",
                                value="correo@example.com",
                                read_only=True
                            ),
                            ft.TextField(
                                label="Contraseña",
                                value="123456",
                                password=True,
                                read_only=True,
                                can_reveal_password=True
                            ),
                            ft.ElevatedButton(
                                text="Editar Información",
                                # on_click=editar_datos_perfil,
                                width=300
                            )
                        ],
                    )
                )
            ],
            spacing=50,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=70
    )