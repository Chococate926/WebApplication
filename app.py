import streamlit as st
import pandas as pd 
import plotly.express as px

st.set_page_config(layout= "wide")
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


df_count_marca = df['marca'].value_counts()

min_ads = st.slider("Minimo de anuncios: ", 0, df_count_marca.max(), 1000)
df_list_marca = df_count_marca[df_count_marca >= min_ads].index

df_marca_filtered = df[df['marca'].isin(df_list_marca)]

button_table = st.button("Mostrar Tabela?")

if button_table:
    st.write("Tabela De Anuncios: ")
    df_marca_filtered



cols1, cols2 = st.columns(2)
cols3, cols4, cols5 = st.columns(3)



df_plot_marca = df_marca_filtered.groupby(['marca', 'type']).size().reset_index(name= "quantidade")

fig_bar = px.bar(
    df_plot_marca,
    x= 'marca',
    y= 'quantidade',
    title= "Marcas e Quantidade",
    color= "type"
)

cols1.plotly_chart(fig_bar)

#histograma

df_marca_filtered_hist = df_marca_filtered.dropna(subset='model_year')


fig_histograma = px.histogram(
    df_marca_filtered_hist,
    title= "Ano do Modelo e Condição",
    x= 'model_year',
    color= 'condition',
    color_discrete_sequence=px.colors.qualitative.Plotly
)

cols2.plotly_chart(fig_histograma)


#Grafico de Dispersão

fig_dispersion = px.scatter(
    df_marca_filtered,
    x= 'odometer',
    y= 'price',
    title= "Grafico de Disperção",
    color_discrete_sequence=px.colors.qualitative.Plotly

)

cols3.plotly_chart(fig_dispersion)

#Condition_transmission_bar

condition_transmission = df_marca_filtered.groupby(['condition', 'transmission']).size().reset_index(name='quantidade')

fig_condition_transmission = px.bar(
    condition_transmission,
    x='condition',
    y='quantidade',
    color='transmission',
    title='Distribuição de Condição por Tipo de Transmissão',
    color_discrete_sequence=px.colors.qualitative.Plotly
)

cols4.plotly_chart(fig_condition_transmission)

#Rodas 4x4
count_4x4 = df_marca_filtered.groupby('is_4wd').size().reset_index(name= 'quantidade')
count_4x4['is_4wd'] = count_4x4['is_4wd'].map(lambda x: '4x4' if x == 1.0 else 'Não 4x4')


fig_barras = px.bar(
    count_4x4,
    x='is_4wd',
    y='quantidade',
    title='Proporção de Veículos com Tração 4x4',
    color='is_4wd',
    color_discrete_sequence=px.colors.qualitative.Plotly
)

cols5.plotly_chart(fig_barras)
