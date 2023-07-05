import streamlit as st

# Título de la aplicación
st.title("Análisis del CSV de Log del Sistema de la Aplicación")

# Explicación de la aplicación
st.markdown("En esta aplicación, analizaremos estadísticas y generaremos visualizaciones basadas en el CSV de logs generados por el uso de la aplicación.")

# Descripción de las secciones
st.header("Secciones de Análisis")
st.markdown("1. **Días de la semana**: Mostrará estadísticas generales sobre la cantidad de operaciones que se realizaron cada día de la semana.")
st.markdown("2. **Uso por género**: Proporcionará información sobre el uso de la aplicación por género.")
st.markdown("3. **Operación**: Analizará la cantidad de operaciones que se realizaron y generará visualizaciones relacionadas.")
st.markdown("4. **Cantidad de operaciones por nick**: Examinará la cantidad de operaciones por nick y mostrará los resultados.")
st.markdown("5. **Imágenes más usadas**: Generará un ranking con las imágenes más usadas tanto para meme como para collage.")
st.markdown("6. **Textos agregados**: En base a los textos agregados tanto en collage como en meme, generará una nube de palabras.")
st.markdown("7. **Uso por géneros en determinadas operaciones**: Reflejará los porcentajes por géneros que realizaron las operaciones 'Nueva imagen clasificada' y 'Modificación de imagen previamente clasificada'.")

# # Instrucciones de uso
# st.header("Instrucciones de Uso")
# st.markdown("1. Seleccione una sección de análisis que se encuentra para ver las estadísticas y visualizaciones relacionadas con ese aspecto específico de los datos.")
# st.markdown("2. Interactúe con los controles y gráficos para explorar los datos y obtener información adicional.")
