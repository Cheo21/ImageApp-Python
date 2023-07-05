import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

ruta_csv = os.path.join('..', 'UnlpImage', 'Assets', 'logs.csv')

df = pd.read_csv(ruta_csv, na_filter=False)

plt.style.use('ggplot')

# Calcular las cantidades de operaciones por nick y desagregarlas en columnas
operaciones_por_nick = df.groupby(['Nick', 'ope']).size().unstack(fill_value=0)

# Configurar los colores para cada operación
colores = ["#FF69B4", "#ECECB3", "#458B00", "#6495ED", "#D8BFD8", "#FFA07A", "#00CED1"]

# Crear el gráfico de barras apilado utilizando DataFrame.plot.barh()
fig, ax = plt.subplots()

operaciones_por_nick.plot.barh(ax=ax,stacked=True, color=colores, legend=False)

plt.title('Operaciones')
fig.set_size_inches(5.65, 2.5)

# Título de la sección
st.header("Análisis de Operaciones por Nick")

# Descripción de la sección
st.markdown("Esta sección muestra un gráfico de barras apilado que muestra las cantidades de operaciones por nick.")

# Barra de selección para mostrar DataFrame o gráfico
opciones = ['Mostrar DataFrame', 'Mostrar Gráfico']
opcion_seleccionada = st.selectbox("Seleccionar opción", opciones)

# Mostrar el DataFrame si se selecciona la opción correspondiente
if opcion_seleccionada == 'Mostrar DataFrame':
    st.write(operaciones_por_nick)

# Mostrar el gráfico si se selecciona la opción correspondiente
if opcion_seleccionada == 'Mostrar Gráfico':
    st.pyplot(fig)
