import PySimpleGUI as sg

# Texto largo
texto_largo = '''
Antes de usar la aplicación para generar memes y collages es necesario hacer las respectivas configuraciones.

¿Qué hace cada botón?

- Foto de perfil (es un CTA): Editar perfil, mostrando la información actual para poder modificar cada campo como sea necesario.

- Configuraciones: Setea y guarda el lugar donde se guardará los collages y donde se buscará los templates de meme.

- Etiquetar Imagen: Permite asociar etiquetas a una imagen.

- Generar MEME: Permite seleccionar entre una lista de templates y a partir de ahí llenar los campos para crear la nueva imagen.

- Generar Collage: Permite crear un collage a partir de varias imágenes guardadas.
'''

def ventana_ayuda():
    # Diseño de la ventana
    layout = [
        [sg.Text(texto_largo)],
        [sg.Button('Cerrar')]
    ]

    # Crear la ventana
    window = sg.Window('Ventana de Ayuda', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Cerrar':
            break

    window.close()
