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

st.set_page_config(layout="wide")
date_format = "%Y-%m-%d"


def import_csv_as_df(csv_file):
    df = pd.read_csv(csv_file)
    return df

def main():
    
    st.title('STER PROJETS')

    # Upload CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        df= import_csv_as_df(uploaded_file)
        print(df.Etat_projet)
        geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
        gdf = gpd.GeoDataFrame(df, geometry=geometry)
        gdf.crs = 'EPSG:4326'
        points_df = gdf[['latitude', 'longitude']]

        map_center = [points_df['latitude'].mean(), points_df['longitude'].mean()]
        m= leafmap.Map(location=map_center, draw_control=False, measure_control=False, zoom=5)    
        

        # for _, row in points_df.iterrows():
        #     leafmap.Marker(
        #         location=[row['latitude'], row['longitude']],
        #         popup=f"Lat: {row['latitude']}, Lon: {row['longitude']}"
        #     ).add_to(m)

        

                #create a marker cluster group for the closest points
        mcg = MarkerCluster()
        for idx, row in gdf.iterrows():
            popup_content = "Id projet: " + str(row["identifiant_projet"])+ "<br>" + "Projet: " + row["projet"] + "<br>" + "Etat: " +row["Etat_projet"]
            if row["Etat_projet"] == "En_attente":
                color= "#FF0000"
            elif row["Etat_projet"] == "En_cours":
                color="#fbff00"
            elif row["Etat_projet"] == "Conclu":
                color="#008000"

            folium.Marker(location=[row['geometry'].y, row['geometry'].x], popup=popup_content, max_width='250',  icon=folium.Icon(icon_color=color)).add_to(mcg)

                # add the marker cluster group to the folium map
        mcg.add_to(m)
        st_folium(m)

if __name__  =='__main__':
    main()
