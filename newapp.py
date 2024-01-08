import streamlit as st
import pandas as pd

# Load the data
def load_data():
    return pd.read_csv('supermarkt_sales.csv')  # Altere o nome do arquivo para o seu arquivo CSV

def main():
    # Load the data
    data = load_data()

    # Set the page configuration
    st.markdown(
        f"""
        <style>
            .reportview-container .main .block-container {{
                max-width: 1200px;
                padding-top: 2rem;
                padding-right: 2rem;
                padding-left: 2rem;
                padding-bottom: 3rem;
            }}
            h1 {{
                text-align: center;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title('Dashboard teste')

    # Abas
    aba1, aba2 = st.tabs(["Base de dados", "Gráficos"])

    with aba1:  
        st.dataframe(data)

        # Sidebar filters
        partner_filter = st.sidebar.multiselect('Selecione o Parceiro:', data['Parceiro'].unique())
        month_options = ['All'] + list(data['Mês'].unique())
        month_filter = st.sidebar.multiselect('Selecione o Mês:', month_options)

        # Check if 'All' is selected
        if 'All' in month_filter:
            # If 'All' is selected, remove other month filters
            month_filter = list(data['Mês'].unique())

        # Filtering the dataframe
        filtered_df = data[data['Parceiro'].isin(partner_filter) & data['Mês'].isin(month_filter)]

        # Display the filtered dataframe with a larger table using st.table
        st.table(filtered_df)

    with aba2:
        # Opções predefinidas para o gráfico
        grafico_options = {
            'Vendas por Mês': {'chart_type': 'line_chart', 'columns': ['Mês', 'Vendas']},
            'Parceiro de Vendas': {'chart_type': 'bar_chart', 'columns': ['Parceiro', 'Vendas']},
            'Quantidade de Vendas por Parceiro': {'chart_type': 'bar_chart', 'columns': ['Parceiro', 'Quantidade']}
        }

        # Selecione a opção para o gráfico
        selected_grafico = st.selectbox('Selecione o tipo de gráfico:', list(grafico_options.keys()))

        # Obtenha as configurações do gráfico selecionado
        selected_chart_settings = grafico_options[selected_grafico]

        # Exiba o gráfico com base nas configurações
        st.subheader(f'{selected_grafico}')
        if selected_chart_settings['chart_type'] == 'line_chart':
            st.line_chart(filtered_df[selected_chart_settings['columns']])
        elif selected_chart_settings['chart_type'] == 'bar_chart':
            st.bar_chart(filtered_df[selected_chart_settings['columns']])

    # Save the modified data to a CSV file
    filtered_df.to_csv('sales_data_filtered.csv', index=False)

if __name__ == '__main__':
    main()
