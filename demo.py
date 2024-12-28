import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
url = "FAOSTAT_data_en_11-25-2024.csv"
df_dash_eu_total = pd.read_csv(url)

# Verificar as primeiras linhas e colunas
st.write(df_dash_eu_total.head())  # Exibir as primeiras linhas
st.write(df_dash_eu_total.columns)  # Exibir as colunas do DataFrame

# Substituir e filtrar dados
df_dash_eu_total['Area'] = df_dash_eu_total['Area'].replace({'Netherlands (Kingdom of the)': 'Netherlands'})
df_dash_eu_total = df_dash_eu_total[df_dash_eu_total['Item'].isin(['Barley', 'Wheat'])]

# Criar pivot_table
dash_df = df_dash_eu_total.pivot_table(index=['Area', 'Year', 'Item'], columns='Element', values='Value', aggfunc='sum').reset_index()
dash_df = dash_df.sort_values(by=['Area', 'Item', 'Year'])

# Definir a página de visualização
def page_1():
    st.title("Page 1: Production and Yield Data")

    # Seletor para ano e item
    col1, col2 = st.columns(2)
    with col1:
        year_selected = st.selectbox("Select Year", dash_df["Year"].unique())
    with col2:
        item_selected = st.selectbox("Select Item", dash_df["Item"].unique())

    filtered_df = dash_df[(dash_df["Item"] == item_selected) & (dash_df["Year"] == year_selected)]
    filtered_df_sorted = filtered_df.sort_values(by="Production", ascending=False)

    # Plotando o gráfico
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(filtered_df_sorted['Area'], filtered_df_sorted['Production'], color='green', label='Production')
    ax1.bar(filtered_df_sorted['Area'], filtered_df_sorted['Area harvested'], color='darkorange', label='Area harvested')
    ax1.set_xlabel('Area')
    ax1.set_ylabel('Production / Area harvested')
    plt.xticks(rotation=45, ha='right')

    ax2 = ax1.twinx()
    ax2.plot(filtered_df_sorted['Area'], filtered_df_sorted['Yield'], color='red', marker='o', label='Yield', linestyle='--', alpha=0.5)
    ax2.set_ylabel('Yield')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

    plt.title(f"Production, Area Harvested, and Yield in {year_selected} for {item_selected}")
    fig.tight_layout()
    st.pyplot(fig)

    # Seletores para Área e Item
    col3, col4 = st.columns(2)
    with col3:
        area_selected_2 = st.selectbox("Select Area", dash_df["Area"].unique())
    with col4:
        item_selected

    filtered_df_year = dash_df[(dash_df["Area"] == area_selected_2) & (dash_df["Item"] == item_selected)]

    # Segundo gráfico
    fig2, ax3 = plt.subplots(figsize=(10, 6))
    ax3.bar(filtered_df_year['Year'], filtered_df_year['Production'], color='green', label='Production')
    ax3.bar(filtered_df_year['Year'], filtered_df_year['Area harvested'], color='darkorange', label='Area harvested')
    ax3.set_xlabel('Year')
    ax3.set_ylabel('Production / Area harvested')
    plt.xticks(rotation=45, ha='right')

    ax4 = ax3.twinx()
    ax4.plot(filtered_df_year['Year'], filtered_df_year['Yield'], color='red', marker='o', label='Yield', linestyle='--', alpha=0.5)
    ax4.set_ylabel('Yield')

    lines3, labels3 = ax3.get_legend_handles_labels()
    lines4, labels4 = ax4.get_legend_handles_labels()
    ax3.legend(lines3 + lines4, labels3 + labels4, loc='upper right')

    plt.title(f"Production, Area Harvested, and Yield in {area_selected_2} for {item_selected_2}")
    fig2.tight_layout()
    st.pyplot(fig2)

page_1()