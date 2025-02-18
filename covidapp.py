import pandas as pd
import plotly.express as px
import streamlit as st


df = pd.read_csv(
    "https://raw.githubusercontent.com/wcota/covid19br/refs/heads/master/cases-brazil-states.csv"
)

df = df.rename(
    columns={
        "newDeaths": "Novos óbitos",
        "newCases": "Novos casos",
        "deaths_per_100k_inhabitants": "Obitos por 100 mil habitantes",
        "totalCases_per_100k_inhabitants": "Casos por 100 mil Habitantes",
        "totalCases": "Casos Totais",
    }
)

# Selecao dos estados
state = "MS"
estados = list(df["state"].unique())

# Selecao dos estados
# column = "Casos por 100 mil Habitantes"
colunas = [
    "Novos óbitos",
    "Novos casos",
    "Obitos por 100 mil habitantes",
    "Casos por 100 mil Habitantes",
]

df = df[df["state"] == state]


state = st.sidebar.selectbox("Escolha o estado", estados)
column = st.sidebar.selectbox("Escolha o estado", colunas)

fig = px.line(df, x="date", y=column, title=column + " - " + state)
fig.update_layout(xaxis_title="Data", yaxis_title=column.upper(), title={"x": 0.5})

st.title("Dados Covida - Brasil")
st.write(
    "Nessa aplicacao os usarios tem a apcao de escolher informacao por tipo e estado"
)


st.plotly_chart(fig, use_container_width=True)
st.caption(
    "Nessa aplicacao os usarios tem a apcao de escolher informacao por tipo e estado"
)
