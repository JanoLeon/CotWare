import flet as ft
import bcrypt
from Conexion_BD.db_conexion import Conexion_BD  # Asegúrate de importar tu clase de conexión

def vista_login(on_login_success):
    def iniciar_sesion(event):
        # Obtener valores de los campos
        email = email_field.value
        password = password_field.value

        # Consultar la base de datos para obtener la contraseña cifrada
        query = "SELECT Contraseña FROM login_empleados WHERE Correo = %s"
        params = (email,)
        cursor = Conexion_BD.get_cursor()
        
        try:
            cursor.execute(query, params)
            result = cursor.fetchone()

            if result:
                # La contraseña cifrada almacenada en la base de datos
                hashed_password = result['Contraseña']
                
                # Verificar si la contraseña ingresada coincide con la cifrada
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    # Si las contraseñas coinciden, navega al menú principal
                    on_login_success()
                else:
                    # Si las credenciales no coinciden
                    print(hashed_password)
                    event.page.snack_bar = ft.SnackBar(ft.Text("Credenciales incorrectas.", color=ft.colors.RED_700))
                    event.page.snack_bar.open = True
                    event.page.update()
            else:
                # Si el correo no existe
                event.page.snack_bar = ft.SnackBar(ft.Text("Correo electrónico no encontrado.", color=ft.colors.RED_700))
                event.page.snack_bar.open = True
                event.page.update()

        except Exception as e:
            # Manejo de errores en la consulta
            print(f"Error al verificar credenciales: {e}")
            event.page.snack_bar = ft.SnackBar(ft.Text("Error al conectar con la base de datos.", color=ft.colors.RED_700))
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
                                            src="icon.png",
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
                    ],
                )
            ],
            spacing=50,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=70
    )
