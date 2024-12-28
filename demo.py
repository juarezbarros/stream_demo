pip install -r requirements.txt
streamlit run seu_script.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title(" Gr")


data = {
    "Ano": [2018, 2019, 2020, 2021, 2022],
    "Vendas": [100, 200, 300, 400, 500]
}


df = pd.DataFrame(data)


st.subheader("Dados de Vendas")
st.dataframe(df)

fig, ax = plt.subplots()
ax.plot(df["Ano"], df["Vendas"], marker='o', linestyle='-', color='blue')
ax.set_title("Vendas por Ano")
ax.set_xlabel("Ano")
ax.set_ylabel("Vendas")


st.pyplot(fig)