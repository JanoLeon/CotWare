import flet as ft

def subir_documento_view(proyectos, regresar_callback):
    proyecto_dropdown = ft.Dropdown(
        label="Seleccionar Proyecto",
        options=[ft.dropdown.Option(proyecto['id']) for proyecto in proyectos],
        width=400
    )

    def archivo_subido(event):
        if event.files:
            if proyecto_dropdown.value is None:
                event.page.snack_bar = ft.SnackBar(ft.Text("Por favor, selecciona un proyecto antes de subir un archivo", color=ft.colors.RED_700))
                event.page.snack_bar.open = True
            else:
                proyecto_id = proyecto_dropdown.value
                event.page.snack_bar = ft.SnackBar(ft.Text(f"Archivo seleccionado para el proyecto ID: {proyecto_id}"))
                event.page.snack_bar.open = True
            event.page.update()

    file_picker = ft.FilePicker(on_result=archivo_subido)

    def subir_archivo(event):
        if proyecto_dropdown.value is None:
            event.page.snack_bar = ft.SnackBar(ft.Text("Por favor, selecciona un proyecto antes de subir un archivo", color=ft.colors.RED_700))
            event.page.snack_bar.open = True
        elif not file_picker.files:
            event.page.snack_bar = ft.SnackBar(ft.Text("Por favor, selecciona un archivo antes de subirlo", color=ft.colors.RED_700))
            event.page.snack_bar.open = True
        else:
            proyecto_id = proyecto_dropdown.value
            archivo_nombre = file_picker.files[0].name
            event.page.snack_bar = ft.SnackBar(ft.Text(f"Archivo '{archivo_nombre}' subido correctamente para el proyecto ID: {proyecto_id}"))
            event.page.snack_bar.open = True
            print("Redirigiendo al menú principal...")
            event.page.update()
            event.page.add(ft.Future.delayed(ft.Duration(seconds=1), lambda: regresar_callback()))

    return ft.Column(
        controls=[
            ft.Text("Subir Documentos para Proyectos", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
            proyecto_dropdown,
            ft.ElevatedButton(
                "Seleccionar Archivo",
                on_click=lambda e: file_picker.pick_files(allow_multiple=False),
                bgcolor=ft.colors.BLUE_600,
                color=ft.colors.WHITE,
                width=200,
            ),
            ft.ElevatedButton(
                "Subir Archivo",
                on_click=subir_archivo,
                bgcolor=ft.colors.BLUE_600,
                color=ft.colors.WHITE,
                width=200,
            ),
            ft.ElevatedButton(
                "Volver al Menú",
                on_click=lambda: regresar_callback(),
                bgcolor=ft.colors.GREY_600,
                color=ft.colors.WHITE,
                width=200,
            ),
            file_picker
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
    )
