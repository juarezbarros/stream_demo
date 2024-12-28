import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


st.title("Dashboard de Produção Agrícola")

# Sidebar para seleção de parâmetros
st.sidebar.title("Parâmetros")
combined_df = pd.read_csv('combined_df.csv')

# Obter áreas e itens únicos do DataFrame
areas = combined_df["Area"].unique()
items = combined_df["Item"].unique()

area_selected = st.sidebar.selectbox("Selecione a Área", areas)
item_selected = st.sidebar.selectbox("Selecione o Item", items)

# Filtrar dados com base na seleção do usuário
filtered_df = combined_df[(combined_df["Area"] == area_selected) & 
                          (combined_df["Item"] == item_selected)]

st.write("### Dados de Produção Filtrados", filtered_df)

st.write("### Gráfico 1")
fig, ax = plt.subplots()
ax.plot(filtered_df["Year"], filtered_df["Production"], label="Production", marker="o")
ax.plot(filtered_df["Year"], filtered_df["Predicted_Production"], label="Predicted Production", 
        linestyle="--", marker="x", color="red")
ax.set_title(f"Produção de {item_selected} em {area_selected}")
ax.set_xlabel("Ano")
ax.set_ylabel("Produção")
ax.legend()
st.pyplot(fig)


st.write("### Gráfico 2")
fig_interactive = px.line(
    filtered_df, 
    x="Year", 
    y=["Production", "Predicted_Production"],
    title=f"Produção de {item_selected} em {area_selected}",
    labels={"value": "Produção", "variable": "Tipo"}
)
st.plotly_chart(fig_interactive)