import streamlit as st
import pandas as pd 
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Data View")
st.header("Anuncios de Carros")

@st.cache_data
def load_data():
    data = pd.read_csv('vehicles.csv')
    data['marca'] = data['model'].str.split().str[0]
    data['is_4wd'] = data['is_4wd'].fillna(0.0)
    data['paint_color'] = data['paint_color'].fillna('unknown')
    data['prob_cylinders'] = data['cylinders'].fillna(data.groupby('model')['cylinders'].transform(lambda x: x.mode()[0]))
    data['date_posted'] = pd.to_datetime(data['date_posted'])
    return data

df = load_data()

# Filtros
min_ads = st.slider("Minimo de anuncios: ", 0, df['marca'].value_counts().max(), 1000)
df_list_marca = df['marca'].value_counts()[df['marca'].value_counts() >= min_ads].index

st.sidebar.header("Filtros")
list_marca = st.sidebar.multiselect("Selecione uma Marca", df_list_marca)
list_types = st.sidebar.multiselect("Selecione um Modelo", df['type'].unique())
list_condition = st.sidebar.multiselect("Selecione uma Condição", df['condition'].unique())
list_transmission = st.sidebar.multiselect("Selecione uma Transmissão", df['transmission'].unique())

preco_range = st.sidebar.slider("Selecione um intervalo de preço", 
                                int(df['price'].min()), 
                                int(df['price'].max()), 
                                (int(df['price'].min()), int(df['price'].max())),
                                1000)

odometer_range = st.sidebar.slider("Selecione um intervalo de odometer", 
                                   int(df['odometer'].min()), 
                                   int(df['odometer'].max()), 
                                   (int(df['odometer'].min()), int(df['odometer'].max())),
                                   100)



df = df[df['marca'].isin(df_list_marca)]



# Aplicando filtros
df_filtered = df[
    (df['marca'].isin(list_marca) if list_marca else True) &
    (df['type'].isin(list_types) if list_types else True) &
    (df['condition'].isin(list_condition) if list_condition else True) &
    (df['transmission'].isin(list_transmission) if list_transmission else True) &
    (df['price'].between(preco_range[0], preco_range[1])) &
    (df['odometer'].between(odometer_range[0], odometer_range[1]))
]

# Botão para mostrar tabela
if st.button("Mostrar Tabela"):
    st.write("Tabela De Anuncios:")
    st.dataframe(df_filtered)

# Container para botões de gráficos
st.header("Visualizações Interativas")
col1, col2 = st.columns(2)

with col1:
    if st.button("Gerar Histograma"):
        fig_hist = px.histogram(df_filtered, x="model_year", color="condition", title="Distribuição de Ano do Modelo por Condição", color_discrete_sequence=px.colors.qualitative.Plotly)
        
        st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    if st.button("Gerar Gráfico de Dispersão"):
        fig_scatter = px.scatter(df_filtered, x="odometer", y="price", title="Relação entre Quilometragem e Preço", color_discrete_sequence=px.colors.qualitative.Plotly)
        
        st.plotly_chart(fig_scatter, use_container_width=True)

# Container para gráficos adicionais com checkboxes
st.header("Análises Detalhadas")
col3, col4, col5 = st.columns(3)

with col3:
    if st.checkbox("Mostrar Distribuição por Marca/Modelo"):
        df_plot = df_filtered.groupby(['marca', 'type']).size().reset_index(name="quantidade")
        
        fig_bar = px.bar(df_plot, x='marca', y='quantidade', color='type', title="Distribuição de Veículos por Marca e Modelo", color_discrete_sequence=px.colors.qualitative.Plotly)
        
        st.plotly_chart(fig_bar, use_container_width=True)

with col4:
    if st.checkbox("Mostrar Distribuição 4x4"):
        count_4x4 = df_filtered.groupby('is_4wd').size().reset_index(name='quantidade')
        count_4x4['is_4wd'] = count_4x4['is_4wd'].map({1.0: '4x4', 0.0: 'Não 4x4'})
        
        fig_4x4 = px.bar(count_4x4, x='is_4wd', y='quantidade', title="Proporção de Veículos com Tração 4x4", color_discrete_sequence=px.colors.qualitative.Plotly, color= 'is_4wd')
        
        
        st.plotly_chart(fig_4x4, use_container_width=True)

with col5:
    if st.checkbox("Mostrar Condição por Transmissão"):
        cond_trans = df_filtered.groupby(['condition', 'transmission']).size().reset_index(name='quantidade')
        
        fig_cond = px.bar(cond_trans, x= 'condition', y= 'quantidade', color= 'transmission', title= "Distribuição de Condição por Transmissão", color_discrete_sequence=px.colors.qualitative.Plotly)
        
        st.plotly_chart(fig_cond, use_container_width=True)