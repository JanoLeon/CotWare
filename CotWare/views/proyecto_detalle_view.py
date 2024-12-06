import flet as ft

def proyecto_detalle_view(proyecto, regresar_callback, ver_horario_callback, actualizar_proyecto_callback):
    # Campos de texto para la edición del proyecto
    nombre_field = ft.TextField(value=proyecto["nombre"], label="Nombre del Proyecto", width=400)
    estado_dropdown = ft.Dropdown(
        label="Estado del Proyecto",
        options=[
            ft.dropdown.Option("Pendiente"),
            ft.dropdown.Option("Aprobado"),
            ft.dropdown.Option("Rechazado"),
        ],
        value=proyecto["estado"],
        width=200,
    )

    # Función para manejar la acción de guardar cambios
    def guardar_cambios(event):
        # Actualizar los datos del proyecto
        proyecto["nombre"] = nombre_field.value
        proyecto["estado"] = estado_dropdown.value
        
        # Llamar al callback para actualizar los datos y la vista principal
        actualizar_proyecto_callback()
        
        # Mostrar una notificación al usuario
        event.page.snack_bar = ft.SnackBar(ft.Text("Proyecto actualizado exitosamente!"))
        event.page.snack_bar.open = True
        event.page.update()

    # Definir la vista con los botones de acción
    return ft.Column(
        controls=[
            ft.Text(f"Detalles del Proyecto {proyecto['id']}", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
            nombre_field,
            estado_dropdown,
            ft.ElevatedButton(
                "Guardar Cambios",
                on_click=guardar_cambios,
                bgcolor=ft.colors.GREEN_600,
                color=ft.colors.WHITE,
                width=200,
            ),
            ft.ElevatedButton(
                "Ver Horario de Trabajadores",
                on_click=lambda _: ver_horario_callback(),
                bgcolor=ft.colors.BLUE_600,
                color=ft.colors.WHITE,
                width=200,
            ),
            ft.ElevatedButton(
                "Volver al Menú",
                on_click=lambda _: regresar_callback(),
                bgcolor=ft.colors.GREY_600,
                color=ft.colors.WHITE,
                width=200,
            ),
        ],
        spacing=20,
    )
