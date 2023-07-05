import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud, STOPWORDS

ruta_csv = os.path.join('..', 'UnlpImage','Assets' ,'logs.csv')

df = pd.read_csv(ruta_csv, na_filter=False)

# Filtrar los textos de los collages y memes
textos_collages = df[df['ope'] == 'new_collage']['text'].dropna()
textos_memes = df[df['ope'] == 'new_meme']['text'].dropna()

# Preprocesar los textos de collages y memes
palabras_collages = [palabra for palabra in textos_collages.tolist() if len(palabra) >= 3]
palabras_memes = [palabra for palabra in textos_memes.tolist() if len(palabra) >= 3]

# Eliminar palabras repetidas
palabras_collages_sinrepetir = set(palabras_collages)
palabras_memes_sinrepetir = set(palabras_memes)

# Filtrar palabras que tengan menor longitud que 3(porque pueden ser conectores)
palabras_collages_sin_conectores = [palabra for palabra in palabras_collages_sinrepetir if len(palabra) >= 3]
palabras_memes_sin_conectores = [palabra for palabra in palabras_memes_sinrepetir if len(palabra) >= 3]

# Convertir los textos en cadenas separadas por espacio
textos_collages = ' '.join(palabras_collages_sin_conectores)
textos_memes = ' '.join(palabras_memes_sin_conectores)

# Función para generar y mostrar la nube de palabras
def plot_cloud(wordcloud):
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud)
    plt.axis('off')
    st.pyplot()

# Desactivar la advertencia de PyplotGlobalUse
st.set_option('deprecation.showPyplotGlobalUse', False)

# Título de la sección
st.header("Nube de Palabras")

# Descripción de la sección
st.markdown("Esta sección muestra una nube de palabras generada a partir de los textos de collages y memes.")

# Barra de selección para mostrar la nube de palabras
opciones = ['Collages', 'Memes']
opcion_seleccionada = st.selectbox("Seleccionar tipo de texto", opciones)

# Generar y mostrar la nube de palabras para collages si se selecciona la opción correspondiente
if opcion_seleccionada == 'Collages':
    st.subheader('Nube de palabras de collages')
    wordcloud_collage = WordCloud(width=200, height=100, random_state=1, background_color='white', colormap='Set2', collocations=False, stopwords=STOPWORDS).generate(textos_collages)
    plot_cloud(wordcloud_collage)

# Generar y mostrar la nube de palabras para memes si se selecciona la opción correspondiente
if opcion_seleccionada == 'Memes':
    st.subheader('Nube de palabras de memes')
    wordcloud_meme = WordCloud(width=200, height=100, random_state=1, background_color='white', colormap='Set2', collocations=False, stopwords=STOPWORDS).generate(textos_memes)
    plot_cloud(wordcloud_meme)
