import streamlit as st
import pandas as pd
from plots import map_chart
from streamlit_folium import st_folium
from helper import init_logging

logger = init_logging(__name__, "heatings_systems.log")


class Buildings():
    def __init__(self):
        self.data = self.get_data()
        self._menu_action = None

        self.menu_options = [
            "Übersicht",
            "Plots",
            "Statistiken",
        ]

        self.menu_icons = [
            "house",
            "person",
            "arrows-fullscreen",
        ]

    @property
    def menu_action(self):
        return self._menu_action
    
    @menu_action.setter
    def menu_action(self, option):
        logger.info(f"Menu action: {option}")
        self._menu_action = option
        if self.menu_options.index(option) == 0:
            self.intro()
        elif self.menu_options.index(option) == 1:
            self.show_plot()
        elif self.menu_options.index(option) == 2:
            self.show_stats()
        else:
            st.error("Invalid menu option.")

    def get_data(self):
        buildings_df = pd.read_csv('./data/100230.csv', sep=';')
        entries_df = pd.read_csv('./data/100231.csv', sep=';')
        entries_df[['lat', 'long']] = entries_df['eingang_koordinaten'].str.split(',', expand=True)
        entries_df['lat'] = pd.to_numeric(entries_df['lat'])
        entries_df['long'] = pd.to_numeric(entries_df['long'])
        entries_df = entries_df[['egid', 'lat', 'long']].groupby('egid').first().reset_index()
        buildings_df = pd.merge(buildings_df, entries_df, on='egid', how='left')
        return buildings_df

    def show_plot(self):
        settings = {
            "width": 1000,
            "height": 800,
            "color": "pink",
        }
        map_chart(self.data, settings)

    def show_stats(self):
        st.write('showing_stats')

    def intro(self):
        st.write('showing_intro')