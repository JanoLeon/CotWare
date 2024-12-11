import flet as ft
from Conexion_BD.db_conexion import Conexion_BD

def subir_documento_view(proyectos, regresar_callback):
    def obtener_proyectos():
        query = "SELECT ID_Proyecto, Nombre_Proyecto FROM proyectos"
        cursor = Conexion_BD.get_cursor()
        cursor.execute(query)
        return cursor.fetchall()

    proyectos = obtener_proyectos()

    proyecto_dropdown = ft.Dropdown(
        label="Seleccionar Proyecto",
        options=[ft.dropdown.Option(proyecto['ID_Proyecto']) for proyecto in proyectos],
        width=400
    )

    archivo_seleccionado = None

    def archivo_subido(event):
        nonlocal archivo_seleccionado
        if event.files:
            archivo_seleccionado = event.files[0]
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
        elif archivo_seleccionado is None:
            event.page.snack_bar = ft.SnackBar(ft.Text("Por favor, selecciona un archivo antes de subirlo", color=ft.colors.RED_700))
            event.page.snack_bar.open = True
        else:
            proyecto_id = proyecto_dropdown.value
            with open(archivo_seleccionado.path, 'rb') as file:
                archivo_contenido = file.read()
            query = "UPDATE proyectos SET Cotizacion_Proyecto = %s WHERE ID_Proyecto = %s"
            cursor = Conexion_BD.get_cursor()
            cursor.execute(query, (archivo_contenido, proyecto_id))
            Conexion_BD.get_connection().commit()
            event.page.snack_bar = ft.SnackBar(ft.Text(f"Archivo subido para el proyecto ID: {proyecto_id}"))
            event.page.snack_bar.open = True
            event.page.update()

    def descargar_archivo(event):
        if proyecto_dropdown.value is None:
            event.page.snack_bar = ft.SnackBar(ft.Text("Por favor, selecciona un proyecto antes de descargar un archivo", color=ft.colors.RED_700))
            event.page.snack_bar.open = True
        else:
            proyecto_id = proyecto_dropdown.value
            query = "SELECT Cotizacion_Proyecto FROM proyectos WHERE ID_Proyecto = %s"
            cursor = Conexion_BD.get_cursor()
            cursor.execute(query, (proyecto_id,))
            archivo_contenido = cursor.fetchone()
            if archivo_contenido and archivo_contenido['Cotizacion_Proyecto']:
                with open(f"archivo_proyecto_{proyecto_id}.pdf", 'wb') as file: # Descargar el archivo subido
                    file.write(archivo_contenido['Cotizacion_Proyecto'])
                event.page.snack_bar = ft.SnackBar(ft.Text(f"Archivo descargado para el proyecto ID: {proyecto_id}"))
                event.page.snack_bar.open = True
            else:
                event.page.snack_bar = ft.SnackBar(ft.Text("No hay archivo para descargar", color=ft.colors.RED_700))
                event.page.snack_bar.open = True
            event.page.update()

    return ft.Column([
        ft.Text("Subir Documento", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
        proyecto_dropdown,
        file_picker, 
        ft.Button("Seleccionar archivo", on_click=lambda _: file_picker.pick_files()),
        ft.Button("Subir archivo", on_click=subir_archivo),
        ft.Button("Descargar archivo", on_click=descargar_archivo),
        ft.Button("Regresar", on_click=regresar_callback)
    ])