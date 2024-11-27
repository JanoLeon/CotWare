import flet as ft
import random

# Lista de mensajes motivadores
motivational_messages = [
    "¡El éxito comienza con la determinación de dar el primer paso!",
    "Cada gran logro empieza con la decisión de intentarlo.",
    "Las oportunidades no pasan, se crean.",
    "El único límite es el que te pones a ti mismo.",
    "No es el tiempo lo que importa, sino lo que haces con él.",
    "Si puedes soñarlo, puedes lograrlo.",
    "La perseverancia es la clave para convertir los sueños en realidad.",
    "El esfuerzo de hoy es el éxito de mañana.",
    "No te detengas hasta estar orgulloso.",
    "Cada pequeño paso te acerca más a tu objetivo.",
]

# Función para obtener un mensaje aleatorio
def get_random_motivational_message():
    return random.choice(motivational_messages)

def Menu_view(toggle_theme):
    return ft.Column(
        controls=[
            # Fila con el título "Bienvenido a COTWARE"
            ft.Row(
                controls=[
                    ft.Text("Bienvenido a COTWARE", size=30, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Centrado horizontalmente
            ),
            # Fila con el texto "Selecciona una opción desde la barra lateral."
            ft.Row(
                controls=[
                    ft.Text("Selecciona una opción desde la barra lateral.", size=18),
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Centrado horizontalmente
            ),
            # Fila con la frase motivacional, tamaño aumentado
            ft.Row(
                controls=[
                    ft.Text(
                        get_random_motivational_message(),
                        size=27,  # Aumentado un 70% respecto al tamaño original de 16
                        weight=ft.FontWeight.BOLD,  # Negrita
                        color=ft.colors.GREY_600,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Centrado tanto en el eje X como en el Y
                expand=True,  # Esto hace que ocupe todo el espacio disponible
            ),
            # Fila con el botón de cambiar tema, alineado a la derecha
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Cambiar Tema",
                        on_click=toggle_theme,
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.BLUE_GREY_500,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,  # Alineación del botón a la derecha
            ),
        ],
        alignment=ft.MainAxisAlignment.START,  # Asegura que la columna esté alineada correctamente
        expand=True,  # Hace que la columna ocupe todo el espacio disponible
    )
