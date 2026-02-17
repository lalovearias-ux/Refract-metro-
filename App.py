import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Refractómetro Virtual", layout="wide")

st.title("🔬 Refractómetro Virtual: Escala Brix")
st.markdown("""
El refractómetro mide el índice de refracción de un líquido. En la industria alimentaria, 
la escala **Brix** se utiliza para medir la cantidad aproximada de azúcares disueltos. 
**1° Brix equivale aproximadamente a 1 gramo de azúcar por cada 100 mL de líquido.**
""")

# --- 1. BASE DE DATOS QUÍMICA ---
# Valores aproximados en grados Brix (g de azúcar / 100 mL)
liquidos = {
    "Agua Destilada": 0.0,
    "Coca-Cola Zero": 0.0,
    "Leche Entera": 4.7,
    "Leche Deslactosada": 4.9, 
    "Gatorade": 6.0,
    "Coca-Cola (Formulación Actual)": 7.5,
    "Sprite": 9.0,
    "Coca-Cola (Original años 90s)": 10.6,
    "Jugo de Manzana Jumex": 11.0,
    "Jugo de Naranja Natural": 11.5,
    "2 Cucharadas de azúcar en 200 ml de agua": 12.5 # ~25g en 200ml
}

# --- 2. INTERFAZ DE USUARIO ---
st.divider()
col_control, col_display = st.columns([1, 1.5])

with col_control:
    st.header("1. Muestra a analizar")
    seleccion = st.selectbox(
        "Coloca unas gotas del líquido en el prisma:", 
        list(liquidos.keys()),
        index=0
    )
    
    brix_val = liquidos[seleccion]
    
    st.header("2. Resultados Analíticos")
    # Tarjetas de resultados estilo métricas
    st.metric(label="Lectura en Escala", value=f"{brix_val:.1f} °Brix")
    st.metric(label="Concentración de Azúcar", value=f"{brix_val:.1f} g / 100 mL")
    st.metric(label="Porcentaje (w/v)", value=f"{brix_val:.1f} %")
    
    # Explicaciones pedagógicas dinámicas
    st.info("💡 **Nota Científica:**")
    if "Zero" in seleccion or "Destilada" in seleccion:
        st.write("Los edulcorantes artificiales (sucralosa, aspartamo) son tan potentes que se usan en cantidades minúsculas. Por eso no desvían la luz significativamente y el refractómetro marca 0.")
    elif "Actual" in seleccion:
        st.write("Debido a las normativas de salud, la formulación actual redujo el azúcar a ~7.5g y compensó el sabor con edulcorantes no calóricos.")
    elif "90s" in seleccion:
        st.write("La fórmula clásica dependía 100% de sacarosa o jarabe de maíz para su dulzor, registrando más de 10g por cada 100mL.")
    elif "Deslactosada" in seleccion:
        st.write("¡Curiosidad! La enzima lactasa rompe la lactosa en glucosa y galactosa. Al haber más partículas disueltas (aunque sea la misma masa), el índice de refracción sube ligeramente comparado con la leche entera.")

# --- 3. MOTOR GRÁFICO DEL REFRACTÓMETRO ---
with col_display:
    st.subheader("👁️ Vista por el Ocular del Refractómetro")
    
    # Configuramos el lienzo
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-16, 16)
    ax.set_ylim(-5, 35)
    ax.set_aspect('equal') # Crucial para que el visor sea un círculo perfecto
    ax.axis('off')
    
    # 1. Crear el visor circular (El campo de visión)
    visor = Circle((0, 15), 15, facecolor='#FFFFFF', edgecolor='#212121', linewidth=8)
    ax.add_patch(visor)
    
    # 2. La sombra azul (El índice de refracción)
    # Cubre desde el valor Brix hasta el tope del visor
    sombra_azul = Rectangle((-15, brix_val), 30, 35-brix_val, facecolor='#1976D2', alpha=0.9)
    sombra_azul.set_clip_path(visor) # Hace que el cuadro azul se corte con la forma del círculo
    ax.add_patch(sombra_azul)
    
    # 3. Dibujar la Escala Central
    ax.plot([0, 0], [0, 30], color='black', linewidth=1.5)
    
    # Marcas (Ticks) de la escala
    for i in range(31):
        if i % 5 == 0:
            # Línea larga cada 5 unidades
            ax.plot([0, 1.5], [i, i], color='black', linewidth=1.5)
            ax.text(2.5, i, f"{i}", va='center', ha='left', fontsize=10, fontweight='bold', color='black')
        else:
            # Línea corta cada 1 unidad
            ax.plot([0, 0.8], [i, i], color='black', linewidth=1)
            
    # Etiqueta de la escala
    ax.text(-3, 15, "B R I X\n%", va='center', ha='right', fontsize=14, fontweight='bold', color='#333333', rotation=90)
    
    # 4. Línea de lectura roja (Ayuda visual)
    linea_lectura = ax.plot([-15, 15], [brix_val, brix_val], color='red', linestyle='--', linewidth=2, alpha=0.8)[0]
    linea_lectura.set_clip_path(visor)
    
    # Renderizamos en Streamlit
    st.pyplot(fig)
