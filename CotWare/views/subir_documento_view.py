import flet as ft

def subir_documento_view(proyectos, regresar_callback):
<<<<<<< HEAD
=======
    # Dropdown para seleccionar el proyecto específico
>>>>>>> 1cf88b35818492218fd7fa699581d04bf529f666
    proyecto_dropdown = ft.Dropdown(
        label="Seleccionar Proyecto",
        options=[ft.dropdown.Option(proyecto['id']) for proyecto in proyectos],
        width=400
    )

<<<<<<< HEAD
    def archivo_subido(event):
        if event.files:
=======
    # Función que maneja el evento de cargar un archivo
    def archivo_subido(event):
        if event.files:
            # Verificar que un proyecto haya sido seleccionado
>>>>>>> 1cf88b35818492218fd7fa699581d04bf529f666
            if proyecto_dropdown.value is None:
                event.page.snack_bar = ft.SnackBar(ft.Text("Por favor, selecciona un proyecto antes de subir un archivo", color=ft.colors.RED_700))
                event.page.snack_bar.open = True
            else:
                proyecto_id = proyecto_dropdown.value
<<<<<<< HEAD
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

=======
                event.page.snack_bar = ft.SnackBar(ft.Text(f"Archivo subido correctamente para el proyecto ID: {proyecto_id}"))
                event.page.snack_bar.open = True
            event.page.update()

    # Botón para seleccionar archivo y FilePicker para la carga
    file_picker = ft.FilePicker(on_result=archivo_subido)

>>>>>>> 1cf88b35818492218fd7fa699581d04bf529f666
    return ft.Column(
        controls=[
            ft.Text("Subir Documentos para Proyectos", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
            proyecto_dropdown,
            ft.ElevatedButton(
                "Seleccionar Archivo",
<<<<<<< HEAD
                on_click=lambda e: file_picker.pick_files(allow_multiple=False),
                bgcolor=ft.colors.BLUE_600,
                color=ft.colors.WHITE,
                width=200,
            ),
            ft.ElevatedButton(
                "Subir Archivo",
                on_click=subir_archivo,
=======
                on_click=lambda e: e.page.file_picker.pick_files(allow_multiple=False),
>>>>>>> 1cf88b35818492218fd7fa699581d04bf529f666
                bgcolor=ft.colors.BLUE_600,
                color=ft.colors.WHITE,
                width=200,
            ),
            ft.ElevatedButton(
                "Volver al Menú",
<<<<<<< HEAD
                on_click=lambda: regresar_callback(),
=======
                on_click=lambda _: regresar_callback(),
>>>>>>> 1cf88b35818492218fd7fa699581d04bf529f666
                bgcolor=ft.colors.GREY_600,
                color=ft.colors.WHITE,
                width=200,
            ),
<<<<<<< HEAD
            file_picker
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
    )
=======
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
    )
>>>>>>> 1cf88b35818492218fd7fa699581d04bf529f666
