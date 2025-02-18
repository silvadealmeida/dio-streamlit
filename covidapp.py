import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import streamlit as st
import requests
import rasterio as rio


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

st.title("Plotly - Dados Covida - Brasil")
st.write(
    "Nessa aplicacao os usarios tem a apcao de escolher informacao por tipo e estado"
)


st.plotly_chart(fig, use_container_width=True)
st.caption(
    "Nessa aplicacao os usarios tem a apcao de escolher informacao por tipo e estado"
)

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?", ("Email", "Home phone", "Mobile phone")
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider("Select a range of values", 0.0, 100.0, (25.0, 75.0))

# Inserir html


# Mapa Testes
st.title("Folium - Teste com Mapas")
############################# mapa 3 - Vectors such as lines
st.title("Vectors such as lines")

# center on Liberty Bell, add marker
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
folium.Marker(
    [39.949610, -75.150282],
    tooltip="Click me!",
    popup="Timberline Lodge",
    icon=folium.Icon(color="green"),
).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)

############################# mapa 2 - Vectors such as lines
st.title("Vectors such as lines")
m = folium.Map(location=[-71.38, -73.9], zoom_start=11)

trail_coordinates = [
    (-71.351871840295871, -73.655963711222626),
    (-71.374144382613707, -73.719861619751498),
    (-71.391042575973145, -73.784922248007007),
    (-71.400964450973134, -73.851042243124397),
    (-71.402411391077322, -74.050048183880477),
]

folium.PolyLine(trail_coordinates, tooltip="Coast").add_to(m)

st_data = st_folium(m, width=725)

############################# mapa 2 - Grouping and controlling
st.title("Grouping and controlling")
m = folium.Map((0, 0), zoom_start=7)

group_1 = folium.FeatureGroup("first group").add_to(m)
folium.Marker((0, 0), icon=folium.Icon("red")).add_to(group_1)
folium.Marker((1, 0), icon=folium.Icon("red")).add_to(group_1)

group_2 = folium.FeatureGroup("second group").add_to(m)
folium.Marker((0, 1), icon=folium.Icon("green")).add_to(group_2)

folium.LayerControl().add_to(m)

st_data = st_folium(m, width=725)

############################# mapa 3 - GeoJSON/TopoJSON overlays
st.title("GeoJSON/TopoJSON overlays")
import requests

m = folium.Map(tiles="cartodbpositron")

geojson_data = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json"
).json()

folium.GeoJson(geojson_data, name="hello world").add_to(m)

folium.LayerControl().add_to(m)

st_data = st_folium(m, width=725)

########################### mapa 4 - Choropleth maps
st.title("Choropleth maps")
import pandas as pd

state_geo = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
).json()
state_data = pd.read_csv(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_unemployment_oct_2012.csv"
)

m = folium.Map(location=[48, -102], zoom_start=3)

folium.Choropleth(
    geo_data=state_geo,
    name="choropleth",
    data=state_data,
    columns=["State", "Unemployment"],
    key_on="feature.id",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Unemployment Rate (%)",
).add_to(m)

folium.LayerControl().add_to(m)

st_data = st_folium(m, width=725)

####################
st.title("Choosing a tileset")
st.write(
    "The default tiles are set to `OpenStreetMap`, but a selection of tilesets are also built in."
)
m = folium.Map((45.5236, -122.6750), tiles="cartodb positron")
folium.LayerControl().add_to(m)


def callback():
    st.toast(f"Current zoom: {st.session_state['my_map']['zoom']}")
    st.toast(f"Current center: {st.session_state['my_map']['center']}")


st_data = st_folium(m, width=725, key="my_map", on_change=callback)
###################
st.title("Com Desenho")
st.write(
    "The default tiles are set to `OpenStreetMap`, but a selection of tilesets are also built in."
)


m = folium.Map(location=[39.949610, -75.150282], zoom_start=5)
Draw(export=True).add_to(m)

c1, c2 = st.columns(2)
with c1:
    output = st_folium(m, width=700, height=500)

with c2:
    st.write(output)

#######
# If you want to dynamically add or remove items from the map,
# add them to a FeatureGroup and pass it to st_folium
fg = folium.FeatureGroup(name="State bounds")
fg.add_child(folium.features.GeoJson(bounds))

capitals = STATE_DATA

for capital in capitals.itertuples():
    fg.add_child(
        folium.Marker(
            location=[capital.latitude, capital.longitude],
            popup=f"{capital.capital}, {capital.state}",
            tooltip=f"{capital.capital}, {capital.state}",
            icon=(
                folium.Icon(color="green")
                if capital.state == st.session_state["selected_state"]
                else None
            ),
        )
    )

out = st_folium(
    m,
    feature_group_to_add=fg,
    center=center,
    width=1200,
    height=500,
)

###################
st.title("Raster")
st.write(
    "The default tiles are set to `OpenStreetMap`, but a selection of tilesets are also built in."
)
# representation of the generated raster
elevRaster = rio.open("elevationClipped.tif")
elevArray = elevRaster.read(1)

boundList = [x for x in elevRaster.bounds]
boundList

# get rid of the nan for color interpretation
elevArray = np.nan_to_num(elevArray)

rasLon = (boundList[3] + boundList[1]) / 2
rasLat = (boundList[2] + boundList[0]) / 2
mapCenter = [rasLon, rasLat]
# Create a Folium map centered at a specific location
m = folium.Map(location=mapCenter, zoom_start=9)

# Add raster overlay
image = folium.raster_layers.ImageOverlay(
    image=elevArray,
    bounds=[[boundList[1], boundList[0]], [boundList[3], boundList[2]]],
    opacity=0.6,
    interactive=True,
    cross_origin=False,
)
image.add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Display the map
st_data = st_folium(m, width=725)

#######
st.write("[https://python-visualization.github.io/folium/latest/getting_started.html]")
st.write("[https://folium.streamlit.app/]")
st.write(
    "(Folium examples )[https://github.com/python-visualization/folium/tree/main/examples]"
)
