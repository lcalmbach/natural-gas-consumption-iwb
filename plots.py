import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import folium
from streamlit_folium import st_folium

MONTHS_REV_DICT = {
    "Jan": 1,
    "Feb": 2,
    "Mrz": 3,
    "Apr": 4,
    "Mai": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Okt": 10,
    "Nov": 11,
    "Dez": 12,
}


def map_chart(df, settings):
    if 'zoom_start' not in settings:
        settings['zoom_start'] = 13
    if 'lat' not in settings:
        settings['lat'] = 'lat'
    if 'long' not in settings:
        settings['long'] = 'long'
    if 'radius' not in settings:
        settings['radius'] = 3
    if 'color' not in settings:
        settings['color'] = 3
    if 'height' not in settings:
        settings['height'] = 600
    if 'width' not in settings:
        settings['width'] = 800
    map_center = df[[settings['lat'], settings['long']]].mean().values.tolist()
    m = folium.Map(location=map_center, zoom_start=settings['zoom_start'])
    df_cleaned = df.dropna(subset=[settings['lat'], 'long'])
    coordinates_list = list(zip(df_cleaned[settings['lat']], df_cleaned[settings['long']]))
    # Add points to the map
    for coord in coordinates_list:
        folium.Circle(
            location=coord,
            radius=settings['radius'],  # radius in meters
            color=settings['color'],
            fill=True,
            fill_color='blue'
        ).add_to(m)

    st_folium(m, height=settings['height'], width=settings['width'])


def chloropleth_chart(df, settings):
    df_plot = df[["BFS_Nummer", settings["selected_variable"]]]
    df_plot.fillna(-1, inplace=True)
    for col in df_plot.columns:
        df_plot[col] = df_plot[col].replace('( )', -1)
        df_plot[col] = df_plot[col].astype('float64')

    # center on Liberty Bell
    coordinates = [47.45, 7.65]
    # coordinates = [43, -100]

    m = folium.Map(location=coordinates, zoom_start=settings["zoom"])
    cp = folium.Choropleth(
        geo_data=settings["var_geojson"],
        name=settings["selected_variable"],
        data=df_plot,
        columns=["BFS_Nummer", settings["selected_variable"]],
        key_on="feature.id",
        fill_color="OrRd",
        fill_opacity=0.8,
        line_opacity=0.2,
        highlight=True,
    ).add_to(m)

    df = df.set_index("BFS_Nummer")
    for s in cp.geojson.data["features"]:
        try:
            value = float(df.loc[s["id"], settings["selected_variable"]])
            s["properties"][settings["selected_variable"]] = value
        except:
            st.write(s["id"])
    folium.GeoJsonTooltip(
        ["Gemeinde", "BFS_Nummer", settings["selected_variable"]]
    ).add_to(cp.geojson)
    folium.LayerControl().add_to(m)
    st_data = st_folium(m, height=settings["height"], width=settings["width"])
    if not st_data["last_active_drawing"] is None:
        return st_data["last_active_drawing"]["id"]
    else:
        return 0

def line_chart(df, settings):
    title = settings["title"] if "title" in settings else ""
    if "x_dt" not in settings:
        settings["x_dt"] = "Q"
    if "y_dt" not in settings:
        settings["y_dt"] = "Q"
    if "x_labels" in settings:
        x_axis = alt.Axis(values=settings["x_labels"])
    else:
        x_axis = alt.Axis()
    if "x_title" not in settings:
        settings["x_title"] = ""
    if "y_title" not in settings:
        settings["y_title"] = ""
    chart = (
        alt.Chart(df)
        .mark_line(width=2, clip=True)
        .encode(
            x=alt.X(
                f"{settings['x']}:{settings['x_dt']}",
                title=settings["x_title"],
                axis=x_axis,
            ),
            y=alt.Y(f"{settings['y']}:{settings['y_dt']}", title=settings["y_title"]),
            color=alt.Color(
                f"{settings['color']}",
                scale=alt.Scale(scheme=alt.SchemeParams(name="rainbow")),
            ),
            tooltip=settings["tooltip"],
        )
    )

    plot = chart.properties(
        width=settings["width"], height=settings["height"], title=title
    )
    st.altair_chart(plot)


def scatter_plot(df, settings):
    title = settings["title"] if "title" in settings else ""
    if "x_labels" in settings:
        x_axis = alt.Axis(values=settings["x_labels"])
    else:
        x_axis = alt.Axis()
    if "x_title" not in settings:
        settings["x_title"] = ""
    if "y_title" not in settings:
        settings["y_title"] = ""

    chart = (
        alt.Chart(df)
        .mark_circle(size=60, clip=True)
        .encode(
            x=alt.X(f"{settings['x']}:Q", title=settings["x_title"], axis=x_axis),
            y=alt.Y(
                f"{settings['y']}:Q",
                title=settings["y_title"],
                scale=alt.Scale(domain=settings["y_domain"]),
            ),
            color=alt.Color(
                f"{settings['color']}",
                scale=alt.Scale(scheme=alt.SchemeParams(name="rainbow")),
                sort=list(const.MONTH_DICT.values()),
            ),
            tooltip=settings["tooltip"],
        )
    )

    line = (
        alt.Chart(df)
        .mark_line(color="red", size=3)
        .transform_window(rolling_mean=f"mean({settings['y']})", frame=[-60, 60])
        .encode(x=settings["x"], y="rolling_mean:Q")
    )

    plot = chart.properties(
        width=settings["width"], height=settings["height"], title=title
    )
    st.altair_chart(plot)


def histogram(df, settings):
    title = settings["title"] if "title" in settings else ""
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(settings["x"], bin=True, title=settings["x_title"]),
            y=alt.Y(settings["y"], title=settings["y_title"]),
        )
    )
    plot = chart.properties(
        width=settings["width"], height=settings["height"], title=title
    )
    st.altair_chart(plot)


def barchart(df, settings):
    title = settings["title"] if "title" in settings else ""
    """
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(f'year:N', axis=alt.Axis(title='', labelAngle=90)),
        y=alt.Y(f'stromverbrauch_kwh:Q', title=settings['y_title'], axis=alt.Axis(grid=False)),
        column = alt.Column('month:N',title=""),
        color='year:N',
        tooltip=settings['tooltip']
        ).configure_view(
            stroke=None,
        )
    """
    sort_field = settings["x"].replace(":Q", "")
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(
                settings["x"],
                title=settings["x_title"],
            ),
            y=alt.Y(
                settings["y"],
                title=settings["y_title"],
                sort=alt.EncodingSortField(field=sort_field, order="descending"),
            ),
            tooltip=settings["tooltip"],
        )
    )
    if "h_line" in settings:
        chart += (
            alt.Chart(df)
            .mark_line()
            .encode(
                x=alt.X(
                    settings["x"],
                    title=settings["x_title"],
                    sort=alt.EncodingSortField(field=sort_field, order="descending"),
                ),
                y=alt.Y(settings["h_line"], title="Mittelwert"),
                color=alt.value("red"),
                tooltip=settings["h_line"],
            )
        )
    plot = chart.properties(
        width=settings["width"], height=settings["height"], title=title
    )
    st.altair_chart(plot)
