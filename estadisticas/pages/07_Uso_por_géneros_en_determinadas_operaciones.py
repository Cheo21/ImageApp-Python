import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import os
import json


ruta_csv = os.path.join('..', 'UnlpImage','Assets' ,'logs.csv')
ruta_json = os.path.join('..', 'UnlpImage','Assets','info_perfil.json')

df = pd.read_csv(ruta_csv,na_filter=False)

#Abrimos el json
with open(ruta_json,encoding="UTF-8") as arch:
    perfiles = json.load(arch)

# Combinar el DataFrame de operaciones con los perfiles usando una columna en común (por ejemplo, 'id')
df_combinado = pd.merge(df, pd.DataFrame(perfiles), on='Nick')

# Filtrar las operaciones específicas
operaciones_clasificadas = df_combinado[df_combinado['ope'] == 'new_image']
operaciones_modificacion = df_combinado[df_combinado['ope'] == 'edit_image']

# Obtener los géneros de las personas que realizaron ambas operaciones
generos_clasificadas = operaciones_clasificadas['Genero']
generos_modificacion = operaciones_modificacion['Genero']

# Calcular los porcentajes de género combinados
porcentaje_generos = pd.concat([generos_clasificadas, generos_modificacion]).value_counts() 

#Creamos figura
fig = plt.figure()

colores = ['#FADBD8', '#D2B4DE', '#F9E79F','#98FB98']
tipos = df_combinado['Genero'].value_counts()

plt.pie(porcentaje_generos,colors= colores,  autopct='%1.1f%%',  startangle=120, labeldistance= 1.1)

plt.axis('equal')

plt.title("Uso por género")

plt.legend(porcentaje_generos.index)

plt.show()

fig.set_size_inches(5.65, 2.5)

# Título de la sección
st.header("Análisis de Género en Operaciones")

# Descripción de la sección
st.markdown("Esta sección muestra un gráfico de torta con los porcentajes según género de las personas que realizaron las operaciones de 'Nueva imagen clasificada' y 'Modificación de imagen previamente clasificada'.")

st.write(fig)

st.markdown("Si desea visualizar la información del DataFrame:")
# Botón para mostrar el DataFrame
show_dataframe = st.button("Mostrar DataFrame")

# Visualización del DataFrame si se hace clic en el botón correspondiente
if show_dataframe:
    st.write(df)