import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import os
import json


# Rutas de los archivos CSV y JSON
ruta_csv = os.path.join('..', 'UnlpImage', 'Assets', 'logs.csv')
ruta_json = os.path.join('..', 'UnlpImage', 'Assets', 'info_perfil.json')

# Lectura del archivo CSV y JSON
df = pd.read_csv(ruta_csv, na_filter=False)
with open(ruta_json, encoding="UTF-8") as arch:
    perfiles = json.load(arch)
df_p = pd.DataFrame(perfiles)

# Combinación de los DataFrames
df_combi = pd.merge(df, df_p, on='Nick')

# Cálculo de los porcentajes de uso por género
generos = df_combi['Genero'].value_counts()

# Configuración del estilo del gráfico
plt.style.use('ggplot')

# Crear el gráfico de porcentajes
fig = plt.figure()

colores = ['#FADBD8', '#D2B4DE', '#F9E79F','#98FB98']
tipos = df_combi['Genero'].value_counts()

plt.pie(generos,colors= colores,  autopct='%1.1f%%',  startangle=120, labeldistance= 1.1)

plt.axis('equal')

plt.title("Uso por género")

plt.legend(generos.index)

plt.show()

fig.set_size_inches(5.65, 2.5)

# Título de la aplicación
st.title("Análisis del uso de la aplicación por género")

# Descripción de la página
st.markdown("En esta página, analizaremos los porcentajes de uso de la aplicación según el género de los usuarios. "
            "Se combinará el archivo de logs con el archivo de perfiles para generar el gráfico correspondiente.")

# Mostrar el DataFrame y el gráfico
st.header("Información de uso por género")
st.write("A continuación, se muestra el DataFrame combinado con información de perfiles y el gráfico de porcentajes "
         "de uso por género.")
st.write(df_combi)
st.write(fig)