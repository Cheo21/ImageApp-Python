import streamlit as st
import pandas as pd 
import os

ruta_csv = os.path.join('..', 'UnlpImage','Assets' ,'logs.csv')

df = pd.read_csv(ruta_csv,na_filter=False)

# Filtrar el DataFrame para obtener las imágenes utilizadas en los memes
imagen_meme = df[df['ope'] == 'new_meme']['valores']

# Filtrar el DataFrame para obtener las imágenes utilizadas en los collages
imagen_collage= df[df['ope'] == 'new_collage']['valores']

# Procesar las imágenes de memes y collages
imagen_meme = imagen_meme.str.split(';').explode().str.strip()

imagen_collage = imagen_collage.str.split(';').explode().str.strip()

# Calcular las 5 imágenes más usadas para memes y collages
mejores5_memes = imagen_meme.value_counts().head()

mejores5_collages = imagen_collage.value_counts().head()

# Título de la página y breve explicación
st.title("Análisis de imágenes más usadas para memes y collages")
st.markdown("Esta página muestra un ranking de las 5 imágenes más utilizadas para generar memes y collages.")


st.subheader('Imágenes más usadas para memes')
# Mostrar la tabla de las 5 imágenes más usadas para memes
st.table(mejores5_memes.reset_index().rename(columns={'index': 'Imagen', 'imagen': 'Usos'}))

st.subheader('Imágenes más usadas para collages')
# Mostrar la tabla de las 5 imágenes más usadas para collages
st.table(mejores5_collages.reset_index().rename(columns={'index': 'Imagen', 'imagen': 'Usos'}))