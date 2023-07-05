import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import os

ruta_csv = os.path.join('..', 'UnlpImage','Assets' ,'logs.csv')

# Cargar el archivo CSV en un DataFrame
df = pd.read_csv(ruta_csv, na_filter=False)

# Establecer el estilo del gráfico
plt.style.use('ggplot')

# Contar la cantidad de cada tipo de operación
cant_ope = df['ope'].value_counts()

# Definir los colores para el gráfico de barras
colores = ["#FF69B4", "#ECECB3", "#458B00", "#6495ED", "#D8BFD8", "#FFA07A", "#00CED1"]

# Crear la figura del gráfico
fig = plt.figure()

# Etiquetas para las operaciones
nombreD = ['chages_config', 'new_meme', 'new_collage', 'edit_image', 'new_image']

# Generar el gráfico de barras
cant_ope.plot(kind='bar', color=colores)

# Título del gráfico
plt.title('Cantidad de Operaciones')

# Rotar las etiquetas del eje x
plt.xticks(rotation=70)

# Ajustar el tamaño de la figura
fig.set_size_inches(5.65, 2.5)

# Título de la sección
st.header("Análisis de Operaciones Realizadas")

# Descripción de la sección
st.markdown("Esta sección muestra un gráfico que refleja las cantidades de cada operación realizada.")

# Botones para mostrar/ocultar el DataFrame y el gráfico
show_dataframe = st.button("Mostrar DataFrame")
show_chart = st.button("Mostrar Gráfico")

# Mostrar el DataFrame si el botón es presionado
if show_dataframe:
    st.write(df)

# Mostrar el gráfico si el botón es presionado
if show_chart:
    st.write(fig)