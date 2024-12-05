import flet as ft

def subir_documento_view(proyectos, regresar_callback):
    # Dropdown para seleccionar el proyecto específico
    proyecto_dropdown = ft.Dropdown(
        label="Seleccionar Proyecto",
        options=[ft.dropdown.Option(proyecto['id']) for proyecto in proyectos],
        width=400
    )

    # Función que maneja el evento de cargar un archivo
    def archivo_subido(event):
        if event.files:
            # Verificar que un proyecto haya sido seleccionado
            if proyecto_dropdown.value is None:
                event.page.snack_bar = ft.SnackBar(ft.Text("Por favor, selecciona un proyecto antes de subir un archivo", color=ft.colors.RED_700))
                event.page.snack_bar.open = True
            else:
                proyecto_id = proyecto_dropdown.value
                event.page.snack_bar = ft.SnackBar(ft.Text(f"Archivo subido correctamente para el proyecto ID: {proyecto_id}"))
                event.page.snack_bar.open = True
            event.page.update()

    # Botón para seleccionar archivo y FilePicker para la carga
    file_picker = ft.FilePicker(on_result=archivo_subido)

    return ft.Column(
        controls=[
            ft.Text("Subir Documentos para Proyectos", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
            proyecto_dropdown,
            ft.ElevatedButton(
                "Seleccionar Archivo",
                on_click=lambda e: e.page.file_picker.pick_files(allow_multiple=False),
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
        alignment=ft.MainAxisAlignment.START,
    )
