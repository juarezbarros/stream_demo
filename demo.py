import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


st.title("Dashboard")


st.sidebar.title("Parameters")
areas = ["Ireland", "Belgium"]
items = ["Wheat", "Barley"]
area_selected = st.sidebar.selectbox("Area", areas)
item_selected = st.sidebar.selectbox("Item", items)


combined_df = pd.read_csv('combined_df.csv')


st.write("### Production Data", df)


st.write("### Graph1")
fig, ax = plt.subplots()
ax.plot(df["Year"], df["Production"], label="Production", marker="o")
ax.plot(df["Year"], df["Predicted Production"], label="Predicted", linestyle="--", marker="x", color="red")
ax.set_title(f"Production of {item_selected} em {area_selected}")
ax.set_xlabel("Year")
ax.set_ylabel("Production")
ax.legend()
st.pyplot(fig)

# Gráph2
st.write("### Graph2")
fig_interactive = px.line(df, x="Year", y=["Production", "Predicted Production"],
                          title=f"Produção de {item_selected} em {area_selected}",
                          labels={"value": "Produção", "variable": "Tipo"})
st.plotly_chart(fig_interactive)