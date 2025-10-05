import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import math

st.set_page_config(
    page_title="Meteor Madness Dashboard",
    layout="wide",
    page_icon="favicon.png"
)

st.image("meteor.png", width=60)
st.title("Meteor Madness: Asteroid Impact Simulator")
st.markdown("Visualize Near-Earth Objects (NEOs) with real NASA data!")

st.sidebar.header("Filter Asteroids")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2015-09-07"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2015-09-08"))
min_diameter = st.sidebar.slider("Min Diameter (m)", 0, 500, 0)
max_speed = st.sidebar.slider("Max Speed (km/s)", 0, 70, 70)

API_KEY = "jugihQb8YqraKaAIizFS5OZyqcQNe2Cx4bwtNs8W"
url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={API_KEY}"
response = requests.get(url)
data = response.json()

neos = []
for date in data['near_earth_objects']:
    for neo in data['near_earth_objects'][date]:
        neos.append({
            "name": neo['name'],
            "diameter_min_m": neo['estimated_diameter']['meters']['estimated_diameter_min'],
            "diameter_max_m": neo['estimated_diameter']['meters']['estimated_diameter_max'],
            "speed_km_s": float(neo['close_approach_data'][0]['relative_velocity']['kilometers_per_second']),
            "miss_distance_km": float(neo['close_approach_data'][0]['miss_distance']['kilometers'])
        })

neos_df = pd.DataFrame(neos)
neos_df = neos_df[(neos_df['diameter_max_m'] >= min_diameter) & (neos_df['speed_km_s'] <= max_speed)]

st.subheader(f"Detected {len(neos_df)} Asteroids in Selected Range")
st.dataframe(neos_df)

DENSITY = 3000
def calculate_stats(row):
    diameter = (row['diameter_min_m'] + row['diameter_max_m']) / 2
    radius = diameter / 2
    volume = (4/3) * math.pi * radius**3
    mass = DENSITY * volume
    speed_m_s = row['speed_km_s'] * 1000
    impact_energy_joules = 0.5 * mass * speed_m_s**2
    tnt_equiv = impact_energy_joules / 4.184e9
    crater_diameter_m = diameter * (mass / 1e6)**(1/3)
    return pd.Series([mass, impact_energy_joules, tnt_equiv, crater_diameter_m])
neos_df[['mass_kg','impact_J','tnt_kt','crater_m']] = neos_df.apply(calculate_stats, axis=1)

meteor_choice = st.sidebar.selectbox("Select an Asteroid for Impact Radius", neos_df['name'])
meteor = neos_df[neos_df['name'] == meteor_choice].iloc[0]
impact_radius_km = meteor['crater_m'] / 2 / 1000

tab1, tab2 = st.tabs(["Overview 🌍", "Asteroid Details ⚡"])

with tab1:
    st.subheader(f"Impact Radius of {meteor_choice}")
    impact_lat, impact_lon = 0, 0  # placeholder
    fig_map = go.Figure()
    fig_map.add_trace(go.Scattergeo(
        lon=[impact_lon], lat=[impact_lat],
        text=[f"{meteor_choice}<br>Impact Radius: {impact_radius_km:.2f} km"],
        marker=dict(size=10, color="red", symbol="circle"),
        name="Impact Center"
    ))
    num_points = 100
    circle_lons = [impact_lon + (impact_radius_km/111) * math.cos(2*math.pi*i/num_points) for i in range(num_points)]
    circle_lats = [impact_lat + (impact_radius_km/111) * math.sin(2*math.pi*i/num_points) for i in range(num_points)]
    fig_map.add_trace(go.Scattergeo(lon=circle_lons, lat=circle_lats, mode='lines', line=dict(color='red', width=2), name='Impact Radius'))
    fig_map.update_layout(geo=dict(showland=True, landcolor="rgb(229, 229, 229)", showcountries=True),
                          height=600, title=f"Impact Radius Visualization for {meteor_choice}")
    st.plotly_chart(fig_map, use_container_width=True)

    st.subheader("Asteroid Global Overview")
    fig_overview = px.scatter_geo(
        neos_df,
        lat=[0]*len(neos_df), lon=[0]*len(neos_df),
        size="tnt_kt", color="speed_km_s",
        hover_name="name",
        hover_data={"diameter_max_m": True, "speed_km_s": True, "tnt_kt": True, "miss_distance_km": True},
        projection="natural earth",
        title="Asteroid Impact Potential (TNT Equivalent in kt)"
    )
    st.plotly_chart(fig_overview, use_container_width=True)

with tab2:
    st.subheader("Asteroid Impact Metrics")
    largest = neos_df.loc[neos_df['diameter_max_m'].idxmax()]
    closest = neos_df.loc[neos_df['miss_distance_km'].idxmin()]
    fastest = neos_df.loc[neos_df['speed_km_s'].idxmax()]
    col1, col2, col3 = st.columns(3)
    col1.metric("Largest Asteroid (m)", f"{largest['diameter_max_m']:.2f}", largest['name'])
    col2.metric("Closest Miss (km)", f"{closest['miss_distance_km']:.0f}", closest['name'])
    col3.metric("Fastest Asteroid (km/s)", f"{fastest['speed_km_s']:.2f}", fastest['name'])
    st.subheader("TNT Equivalent Bar Chart")
    fig_bar = px.bar(neos_df.sort_values('tnt_kt', ascending=False).head(10),
                     x='name', y='tnt_kt', color='tnt_kt', color_continuous_scale='Reds',
                     title="Top 10 Asteroids by TNT Equivalent (kt)")
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")
st.markdown("Data Source: [NASA NEO API](https://api.nasa.gov/)")
