import streamlit as st
import pandas as pd
import altair as alt

def set_page_config():
    st.set_page_config(
        page_title="Dashboard Teste",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def load_data():
    return pd.read_csv('supermarkt_sales.csv')  # Altere o nome do arquivo para o seu arquivo CSV

def filter_data(data, partner_filter, month_filter):
    if 'All' in month_filter:
        month_filter = list(data['Mês'].unique())

    filtered_df = data[data['Parceiro'].isin(partner_filter) & data['Mês'].isin(month_filter)]

    return filtered_df

def display_filtered_data(filtered_df):
    st.table(filtered_df)

def create_chart(filtered_df, chart_type, x_column, y_column):
    chart = alt.Chart(filtered_df).mark_bar().encode(
        x=x_column,
        y=y_column
    ).interactive()

    return chart

def render_charts(filtered_df, chart_type, x_column, y_column):
    chart = create_chart(filtered_df, chart_type, x_column, y_column)
    st.altair_chart(chart, use_container_width=True)

def main():
    set_page_config()
    st.title('Dashboard teste')

    # Load the data
    data = load_data()

    # Filter the data
    partner_filter = st.sidebar.multiselect('Selecione o Parceiro:', data['Parceiro'].unique())
    month_options = ['All'] + list(data['Mês'].unique())
    month_filter = st.sidebar.multiselect('Selecione o Mês:', month_options)

    # Display the filtered data in the first tab
    filtered_df = filter_data(data, partner_filter, month_filter)
    with st.expander("Dados Filtrados"):
        display_filtered_data(filtered_df)

    # Create and render the charts in the second tab
    with st.expander("Gráficos"):
        st.subheader("Selecione o tipo de gráfico:")
        chart_options = {
            'Vendas por Parceiro': {'chart_type': 'bar_chart', 'x_column': 'Parceiro', 'y_column': 'N° de vendas'},
            'Vendas por Mês': {'chart_type': 'bar_chart', 'x_column': 'Mês', 'y_column': 'N° de vendas'},
            'GMV por Parceiro': {'chart_type': 'bar_chart', 'x_column': 'Parceiro', 'y_column': 'GMV'}
        }
        selected_chart = st.selectbox('Selecione o tipo de gráfico:', list(chart_options.keys()))
        chart_settings = chart_options[selected_chart]

        if chart_settings['x_column'] in filtered_df.columns and chart_settings['y_column'] in filtered_df.columns:
            render_charts(filtered_df, chart_settings['chart_type'], chart_settings['x_column'], chart_settings['y_column'])
        else:
            st.warning("Selecione uma combinação válida de colunas para gerar o gráfico.")

    # Salvar os dados modificados em um arquivo CSV
    filtered_df.to_csv('sales_data_filtered.csv', index=False)

if __name__ == "__main__":
    main()
