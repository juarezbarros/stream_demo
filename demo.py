import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
url = "FAOSTAT_data_en_11-25-2024.csv"
df_dash_eu_total = pd.read_csv(url)



df_dash_eu_total['Area'] = df_dash_eu_total['Area'].replace({'Netherlands (Kingdom of the)': 'Netherlands'})
df_dash_eu_total = df_dash_eu_total[df_dash_eu_total['Item'].isin(['Barley', 'Wheat'])]


dash_df = df_dash_eu_total.pivot_table(index=['Area', 'Year', 'Item'], columns='Element', values='Value', aggfunc='sum').reset_index()
dash_df = dash_df.sort_values(by=['Area', 'Item', 'Year'])

def page_1():
    st.title("Production, Harvested and Yield Data")

    # Seletor para ano e item
    col1, col2 = st.columns(2)
    with col1:
        year_selected = st.selectbox("Select Year", dash_df["Year"].unique())
    with col2:
        item_selected = st.selectbox("Select Item", dash_df["Item"].unique())

    # Gráfico 1
    filtered_df = dash_df[(dash_df["Item"] == item_selected) & (dash_df["Year"] == year_selected)]
    filtered_df_sorted = filtered_df.sort_values(by="Production", ascending=False)

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(filtered_df_sorted['Area'], filtered_df_sorted['Production'], color='green', label='Production', alpha=0.8)
    ax1.bar(filtered_df_sorted['Area'], filtered_df_sorted['Area harvested'], color='darkorange', label='Area harvested')
    ax1.set_xlabel('Area')
    ax1.set_ylabel('Production / Area harvested')
    plt.xticks(rotation=45, ha='right')

    ax2 = ax1.twinx()
    ax2.plot(filtered_df_sorted['Area'], filtered_df_sorted['Yield'], color='red', marker='o', label='Yield', linestyle='--')
    ax2.set_ylabel('Yield')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

    plt.title(f"Production, Area Harvested, and Yield in {year_selected} for {item_selected}")
    fig.tight_layout()
    st.pyplot(fig)

    # Comparação de dois países
    st.subheader("Country Comparison")
    col3, col4 = st.columns(2)
    with col3:
        country_1 = st.selectbox("Select First Country", dash_df["Area"].unique(), key="country1")
    with col4:
        country_2 = st.selectbox("Select Second Country", dash_df["Area"].unique(), key="country2")

    filtered_df_1 = dash_df[(dash_df["Area"] == country_1) & (dash_df["Item"] == item_selected)]
    filtered_df_2 = dash_df[(dash_df["Area"] == country_2) & (dash_df["Item"] == item_selected)]

    # Criar gráficos lado a lado com duas escalas y
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

    # País 1
    ax1 = axes[0]
    ax1.bar(filtered_df_1['Year'], filtered_df_1['Production'], color='green', label='Production', alpha=0.8)
    ax1.bar(filtered_df_1['Year'], filtered_df_1['Area harvested'], color='darkorange', label='Area harvested')
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Production / Area harvested")
    ax1.legend()

    ax2 = ax1.twinx()  # Adiciona o eixo Y para o Yield
    ax2.plot(filtered_df_1['Year'], filtered_df_1['Yield'], color='red', marker='o', label='Yield', linestyle='--')
    ax2.set_ylabel("Yield")
    
    # País 2
    ax3 = axes[1]
    ax3.bar(filtered_df_2['Year'], filtered_df_2['Production'], color='green', label='Production', alpha=0.8)
    ax3.bar(filtered_df_2['Year'], filtered_df_2['Area harvested'], color='darkorange', label='Area harvested')
    ax3.set_xlabel("Year")
    ax3.set_ylabel("Production / Area harvested")
    ax3.legend()

    ax4 = ax3.twinx()  # Adiciona o eixo Y para o Yield
    ax4.plot(filtered_df_2['Year'], filtered_df_2['Yield'], color='red', marker='o', label='Yield', linestyle='--')
    ax4.set_ylabel("Yield")

    # Ajustar layout
    fig.suptitle(f"Comparison of {country_1} and {country_2} for {item_selected}")
    fig.tight_layout()
    st.pyplot(fig)

def page_pie_chart():
    st.title("Proportions by Country")

    # Seletor de ano e item
    col5, col6 = st.columns(2)
    with col5:
        year_selected = st.selectbox("Select Year for Pie Chart", dash_df["Year"].unique())
    with col6:
        item_selected = st.selectbox("Select Item for Pie Chart", dash_df["Item"].unique())

    # Filtrar os dados
    filtered_df = dash_df[(dash_df["Year"] == year_selected) & (dash_df["Item"] == item_selected)]

    # Verificar se há dados
    if filtered_df.empty:
        st.warning("No data available for the selected year and item.")
    else:
        # Calcular proporção
        filtered_df["Proportion"] = filtered_df["Production"] / filtered_df["Production"].sum()

        # Gráfico de pizza
        fig = px.pie(filtered_df, values="Proportion", names="Area",
                     title=f"Proportion of Production by Country in {year_selected} for {item_selected}",
                     labels={"Proportion": "Proportion"})
        st.plotly_chart(fig)

# Configuração do Streamlit
page = st.sidebar.radio("Select Page", ["Page 1", "Pie Chart"])

if page == "Historical Data":
    page_1()
elif page == "Pie Chart":
    page_pie_chart()