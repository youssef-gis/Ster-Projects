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
from ipyleaflet import Map, basemaps, WidgetControl
from ipywidgets import IntSlider, ColorPicker, jslink


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
        print(df.columns)
        geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
        gdf = gpd.GeoDataFrame(df, geometry=geometry)
        gdf.crs = 'EPSG:4326'
        points_df = gdf[['latitude', 'longitude']]

        map_center = [points_df['latitude'].mean(), points_df['longitude'].mean()]
        m= leafmap.Map(location=map_center, draw_control=False, measure_control=False, zoom=5 )
        zoom_slider = IntSlider(description='Zoom level:', min=0, max=15, value=7)
        #jslink((zoom_slider, 'value'), (m, 'zoom'))
        widget_control1 = WidgetControl(widget=zoom_slider, position='topright')
        m.add(widget_control1)
 
                #create a marker cluster group for the closest points
        mcg = MarkerCluster()
        for idx, row in gdf.iterrows():
            popup_content = "<b>"+"Id projet: "+"</b>" + str(row["identifiant_projet"])+ "<br>" +  "<b>"+"Projet: "+"</b>"  + row["projet"] + "<br>" +"<b>"+ "Etat: "+"</b>" +row["Etat_projet"]
            if row["Etat_projet"] == "En_attente":
                color= "#FF0000"
            elif row["Etat_projet"] == "En_cours":
                color="#fbff00"
            elif row["Etat_projet"] == "Conclu":
                color="#008000"

            folium.Marker(location=[row['geometry'].y, row['geometry'].x], tooltip=row['identifiant_projet'],popup=folium.Popup(popup_content, parse_html=False, max_width="1000"),  icon=folium.Icon(icon_color=color)).add_to(mcg)

                # add the marker cluster group to the folium map
        mcg.add_to(m)
        m.to_streamlit()

if __name__  =='__main__':
    main()

