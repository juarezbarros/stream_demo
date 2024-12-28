import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

df_dash_eu_total=pd.read_csv("FAOSTAT_data_en_12_5_2024.csv")
df_dash_eu_total = df_dash_eu_total[df_dash_eu_total['Item'].isin(['Barley', 'Wheat'])]

dash_df = df_dash_eu_total.pivot_table(index=['Area', 'Year', 'Item'], columns='Element', values='Value', aggfunc='sum'
).sort_values(by='Production', ascending=False).reset_index()

dash_df = dash_df.sort_values(by=['Area', 'Item', 'Year'])

st.title("Agriculture Dashboard")
pivoted_df = dash_df


st.sidebar.title("Parameters")
years = pivoted_df["Year"].unique()  # Obter anos únicos
items = pivoted_df["Item"].unique()  # Obter itens únicos (ex: "Wheat", "Barley")

year_selected = st.sidebar.selectbox("Select Year", years)
item_selected = st.sidebar.selectbox("Select Item", items)


df_filtered = pivoted_df[(pivoted_df["Year"] == year_selected) & (pivoted_df["Item"] == item_selected)]


df_filtered = df_filtered.sort_values(by='Production', ascending=False)


st.write(f"### Productio Data for the Year {year_selected} and Item {item_selected}", df_filtered)


fig, ax1 = plt.subplots(figsize=(10, 6))


ax1.bar(df_filtered['Area'], df_filtered['Production'], color='green', label='Production')
ax1.bar(df_filtered['Area'], df_filtered['Area harvested'], color='darkorange', label='Area harvested')
ax1.set_xlabel('Country')
ax1.set_ylabel('Production / Area harvested')


ax2 = ax1.twinx()
ax2.plot(df_filtered['Area'], df_filtered['Yield'], color='red', marker='o', label='Yield', linestyle='--', alpha=0.5)
ax2.set_ylabel('Yield')


plt.xticks(rotation=90, ha='right', fontsize=10)


lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')


plt.title(f'Production, Area harvested e Yield per Year {year_selected} and Item {item_selected}')
fig.tight_layout()  


st.pyplot(fig)