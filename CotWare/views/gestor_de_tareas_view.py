import flet as ft

# Lista global de tareas
tareas = []

# Función para agregar una tarea
def agregar_tarea(tarea_input: ft.TextField, lista_tareas: ft.Column, page: ft.Page):
    if tarea_input.value != "":
        tareas.append({"tarea": tarea_input.value, "completada": False})
        tarea_input.value = ""  # Limpiar el campo de texto después de agregar la tarea
        tarea_input.focus()  # Mantener el foco en el campo de texto
        actualizar_lista_tareas(lista_tareas, page)  # Actualizar la lista de tareas y la página

# Función para marcar una tarea como completada
def completar_tarea(index: int, lista_tareas: ft.Column, page: ft.Page):
    tareas[index]["completada"] = not tareas[index]["completada"]
    actualizar_lista_tareas(lista_tareas, page)  # Actualizar la lista de tareas y la página

# Función para eliminar una tarea
def eliminar_tarea(index: int, lista_tareas: ft.Column, page: ft.Page):
    tareas.pop(index)
    actualizar_lista_tareas(lista_tareas, page)  # Actualizar la lista de tareas y la página

# Función para actualizar la lista de tareas mostrada
def actualizar_lista_tareas(lista_tareas: ft.Column, page: ft.Page):
    lista_tareas.controls.clear()  # Limpiar la lista de tareas antes de actualizar
    for i, tarea in enumerate(tareas):
        tarea_text = tarea["tarea"]
        if tarea["completada"]:
            tarea_text = f"✅ {tarea_text}"  # Marcar tareas completadas con un símbolo de verificación

        tarea_card = ft.Row(
            controls=[
                ft.Text(tarea_text),
                ft.IconButton(ft.icons.CHECK, on_click=lambda e, index=i: completar_tarea(index, lista_tareas, page)),
                ft.IconButton(ft.icons.DELETE, on_click=lambda e, index=i: eliminar_tarea(index, lista_tareas, page))
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        lista_tareas.controls.append(tarea_card)

    page.update()  # Actualizar la página después de modificar los controles

# Vista principal para organizar tareas
def Gestor_de_tareas_view(page: ft.Page):
    # Crear una columna para mostrar las tareas
    lista_tareas = ft.Column(expand=True)

    # Campo de texto para ingresar nuevas tareas
    tarea_input = ft.TextField(label="Nueva tarea", on_submit=lambda e: agregar_tarea(tarea_input, lista_tareas, page))

    # Actualizar la lista de tareas en la vista
    actualizar_lista_tareas(lista_tareas, page)

    # Devolver la vista con el formulario y la lista de tareas
    return ft.Column(
        controls=[
            tarea_input,
            lista_tareas,
        ]
    )
