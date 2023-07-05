import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Ruta del archivo CSV de logs
ruta_csv = os.path.join('..', 'UnlpImage', 'Assets', 'logs.csv')

# Lectura del archivo CSV
df = pd.read_csv(ruta_csv, na_filter=False)

# Estilo de gráficos
plt.style.use('ggplot')

# Conversión del campo de tiempo a formato de fecha
df['fecha'] = df['time'].apply(lambda x: datetime.fromtimestamp(x))

# Extracción del nombre del día de la semana
df['dia'] = df['fecha'].dt.day_name()

# Nombres de los días en orden
nombres_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Conteo de operaciones por día
operaciones_por_dia = df.groupby('dia').size()
operaciones_por_dia = operaciones_por_dia.reindex(nombres_dias, fill_value=0)

# Colores para cada barra del gráfico
colores = ["#FF69B4", "#ECECB3", "#458B00", "#6495ED", "#D8BFD8", "#FFA07A", "#00CED1"]

# Creación del gráfico de barras

fig = plt.figure()

nombreD = ['L','M','M','J','V','S','D']

plt.bar(nombreD, operaciones_por_dia,color = colores)

plt.title('Operaciones')

fig.set_size_inches(5.65, 2.5)

# Título de la aplicación
st.title("Análisis de los días de la semana en que se realizaron operaciones")

# Explicación de la aplicación
st.markdown("Esta aplicación muestra un gráfico comparativo de los días de la semana en los que se realizaron operaciones, junto con el DataFrame utilizado para generar el gráfico.")

st.markdown("Si desea visualizar la información del DataFrame:")
# Botón para mostrar/ocultar el DataFrame
show_dataframe = st.button("Mostrar DataFrame")

st.markdown("Si desea visualizar el gráfico:")
# Botón para mostrar/ocultar el gráfico
show_chart = st.button("Mostrar Gráfico")

# Visualización del DataFrame si se hace clic en el botón correspondiente
if show_dataframe:
    st.write(df)

if show_chart:
    st.write(fig)