import flet as ft

def vista_login(on_login_success, toggle_theme):
    def iniciar_sesion(event):
        # Validar las credenciales del usuario
        email = email_field.value
        password = password_field.value
        # Suponiendo que las credenciales son correctas
        if email == "correo@correo.cl" and password == "contraseña":  # Cambia esto por tu lógica de autenticación
            on_login_success()  # Llama a la función para navegar al menú principal
        else:
            event.page.snack_bar = ft.SnackBar(ft.Text("Credenciales incorrectas.", color=ft.colors.RED_700))
            event.page.snack_bar.open = True
            event.page.update()

    email_field = ft.TextField(
        icon=ft.icons.LABEL_SHARP,
        label="Correo electrónico",
        value="",
        expand=True
    )
    
    password_field = ft.TextField(
        icon=ft.icons.LABEL,
        label="Contraseña",
        value="",
        password=True,  # Esto oculta el texto de la contraseña
        expand=True
    )
    
    return ft.Container(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Card(
                            ft.Container(
                                ft.Column(
                                    [
                                        ft.Image(
                                            src="logo_proyecto.jpeg",
                                            fit=ft.ImageFit.CONTAIN
                                        ),
                                        ft.Divider(),
                                        email_field,
                                        password_field,
                                        ft.Row(
                                            [
                                                ft.ElevatedButton(
                                                    "Iniciar Sesión",
                                                    on_click=iniciar_sesion,
                                                    expand=True
                                                )
                                            ]
                                        ),
                                    ],
                                ),
                                width=400,
                                padding=10,
                            )
                        ),
                        # ft.Row(
                        #     [
                        #         ft.ElevatedButton(
                        #             "Cambiar Tema",
                        #             on_click=toggle_theme,
                        #             style=ft.ButtonStyle(
                        #                 color=ft.colors.WHITE,
                        #                 bgcolor=ft.colors.BLUE_GREY_500,
                        #             ),
                        #         ),
                        #     ],
                        #     alignment=ft.MainAxisAlignment.START,  # Alineación del botón a la izquierda
                        # ),
                    ],
                )
            ],
            spacing=50,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=70
    )