import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
url = "https://raw.githubusercontent.com/juarezbarros/stream_demo/main/FAOSTAT_data_en_11-25-2024.csv"
df_dash_eu_total = pd.read_csv(url)

df_dash_eu_total = df_dash_eu_total[df_dash_eu_total['Item'].isin(['Barley', 'Wheat'])]
dash_df = df_dash_eu_total.pivot_table(index=['Area', 'Year', 'Item'], columns='Element', values='Value', aggfunc='sum'
).sort_values(by='Production', ascending=False).reset_index()
dash_df = dash_df.sort_values(by=['Area', 'Item', 'Year'])

def page_1():
    st.title("Page 1: Production and Yield Data")

    
    area_selected = st.sidebar.selectbox("Select Area", df_dash_eu_total["Area"].unique())
    item_selected = st.sidebar.selectbox("Select Item", df_dash_eu_total["Item"].unique())

    
    filtered_df = dash_df[(dash_df["Area"] == area_selected) & 
                                   (dash_df["Item"] == item_selected)]

    
    st.write(filtered_df.head())

    
    fig, ax1 = plt.subplots(figsize=(10, 6))

    
    ax1.bar(filtered_df['Area'], filtered_df['Production'], color='green', label='Production')
    ax1.bar(filtered_df['Area'], filtered_df['Area harvested'], color='darkorange', label='Area harvested')
    ax1.set_xlabel('Country')
    ax1.set_ylabel('Production / Area harvested')

    
    plt.xticks(rotation=45, ha='right')

   
    ax2 = ax1.twinx()
    ax2.plot(filtered_df['Area'], filtered_df['Yield'], color='red', marker='o', label='Yield', linestyle='--', alpha=0.5)
    ax2.set_ylabel('Yield')

    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

    
    plt.title(f"Production, Area Harvested, and Yield in {area_selected} for {item_selected}")

    
    fig.tight_layout()

    
    st.pyplot(fig)

    
    st.write("### Production, Area Harvested, and Yield by Year")
    
    
    filtered_df_year = df_dash_eu_total[(df_dash_eu_total["Item"] == item_selected)]

    
    fig2, ax3 = plt.subplots(figsize=(10, 6))

    
    ax3.bar(filtered_df_year['Year'], filtered_df_year['Production'], color='green', label='Production')
    ax3.bar(filtered_df_year['Year'], filtered_df_year['Area harvested'], color='darkorange', label='Area harvested')
    ax3.set_xlabel('Year')
    ax3.set_ylabel('Production / Area harvested')

    
    plt.xticks(rotation=45, ha='right')

    # Criando o segundo eixo Y para 'Yield'
    ax4 = ax3.twinx()
    ax4.plot(filtered_df_year['Year'], filtered_df_year['Yield'], color='red', marker='o', label='Yield', linestyle='--', alpha=0.5)
    ax4.set_ylabel('Yield')

    
    lines3, labels3 = ax3.get_legend_handles_labels()
    lines4, labels4 = ax4.get_legend_handles_labels()
    ax3.legend(lines3 + lines4, labels3 + labels4, loc='upper right')

    
    plt.title(f"Production, Area Harvested, and Yield for {item_selected} Over the Years")

    
    fig2.tight_layout()

    
    st.pyplot(fig2)


page_1()