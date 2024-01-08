import streamlit as st
import pandas as pd
import altair as alt

# Função para carregar os dados
def load_data():
    return pd.read_csv('supermarkt_sales.csv')  # Altere o nome do arquivo para o seu arquivo CSV

# Função para criar o gráfico de barras
def create_bar_chart(data, x_column, y_column, title):
    chart = alt.Chart(data).mark_bar().encode(
        x=x_column,
        y=y_column
    ).properties(
        title=title
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

def main():
    # Carregar dados
    data = load_data()

    # Configurações da página
    st.set_page_config(
        page_title='Dashboard de Vendas',
        layout='wide'
    )

    st.title('Dashboard de Vendas')

    # Abas
    aba1, aba2 = st.columns(2)

    with aba1:
        st.header('Base de dados')

        # Filtros
        st.sidebar.header('Filtros')
        partner_filter = st.sidebar.multiselect('Selecione o Parceiro:', data['Parceiro'].unique())
        month_filter = st.sidebar.multiselect('Selecione o Mês:', data['Mês'].unique())
        gmv_range = st.sidebar.slider('Selecione Faixa de GMV:', float(data['GMV'].min()), float(data['GMV'].max()), (float(data['GMV'].min()), float(data['GMV'].max())))

        # Aplicar filtros
        filtered_df = data[data['Parceiro'].isin(partner_filter) & data['Mês'].isin(month_filter) & (data['GMV'] >= gmv_range[0]) & (data['GMV'] <= gmv_range[1])]

        # Exibir dados filtrados
        st.dataframe(filtered_df)

    with aba2:
        st.header('Gráficos')

        # Gráficos disponíveis
        grafico_options = {
            'Vendas por Parceiro': {'x_column': 'Parceiro', 'y_column': 'N° de vendas'},
            'Vendas por Mês': {'x_column': 'Mês', 'y_column': 'N° de vendas'},
            'GMV por Parceiro': {'x_column': 'Parceiro', 'y_column': 'GMV'}
        }

        # Selecione o tipo de gráfico
        selected_grafico = st.selectbox('Selecione o tipo de gráfico:', list(grafico_options.keys()))

        # Crie o gráfico correspondente
        create_bar_chart(filtered_df, grafico_options[selected_grafico]['x_column'],
                         grafico_options[selected_grafico]['y_column'], selected_grafico)

    # Salvar os dados filtrados em um arquivo CSV
    filtered_df.to_csv('sales_data_filtered.csv', index=False)

if __name__ == '__main__':
    main()
