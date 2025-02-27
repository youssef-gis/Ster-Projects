import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import leafmap.foliumap as leafmap
from shapely.geometry import Point
import folium
from folium.plugins import Geocoder, Fullscreen
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium, folium_static
import plotly.express as px

st.set_page_config(layout="wide")
date_format = "%Y-%m-%d"

@st.cache_resource
def import_csv_as_df(csv_file):
    df = pd.read_csv(csv_file)
    return df

def main():
    
    st.title('STER PROJETS')

    # Upload CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        df= import_csv_as_df(uploaded_file)
        
        geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
        gdf = gpd.GeoDataFrame(df, geometry=geometry)
        gdf.crs = 'EPSG:4326'
        points_df = gdf[['latitude', 'longitude']]
        # Create columns
        col1, col2 = st.columns(2)

        # Add content to the first column
        with col1:

            map_center = [points_df['latitude'].mean(), points_df['longitude'].mean()]
            m= leafmap.Map(location=map_center, draw_control=False, measure_control=False, zoom=5 )
    
                    #create a marker cluster group for the closest points
            mcg = MarkerCluster(name="Projets")
            for idx, row in gdf.iterrows():
                popup_content = "<b>"+"Id projet: "+"</b>" + str(row["identifiant_projet"])+ "<br>" +  "<b>"+"Projet: "+"</b>"  + row["projet"] + "<br>" +"<b>"+ "Etat: "+"</b>" +row["Etat_projet"]
                if row["Etat_projet"] == "En_attente":
                    color= "#FF0000"
                elif row["Etat_projet"] == "En_cours":
                    color="orange"
                elif row["Etat_projet"] == "Conclu":
                    color="#008000"

                folium.Marker(location=[row['geometry'].y, row['geometry'].x], tooltip=row['identifiant_projet'],popup=folium.Popup(popup_content, parse_html=False, max_width="1000"),  icon=folium.Icon(icon_color=color, icon='home')).add_to(mcg)

                    # add the marker cluster group to the folium map
            mcg.add_to(m)
            m.to_streamlit()

        # Add content to the second column
        with col2:
            st.header('Pie Chart')

            # Aggregate data: Count occurrences of each category
            category_counts = df['Etat_projet'].value_counts().reset_index()
            category_counts.columns = ['Etat_projet', 'Count']
            print(category_counts)
            # Define custom colors for each category
            color_map = {
                "En_cours": "orange",
                "En_attente": "red",
                "Conclu": "green"
            }
            # Create a pie chart using Plotly Express
            fig = px.pie(category_counts, names='Etat_projet', values='Count',  color='Etat_projet',color_discrete_map=color_map,
   
             hole=0.3  # Create a donut chart with a hole in the cent,
            )

            # Display the pie chart in the Streamlit app
            st.plotly_chart(fig)
           




if __name__  =='__main__':
    main()
