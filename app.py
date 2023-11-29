import streamlit as st
from streamlit_option_menu import option_menu
from buildings import Buildings
from helper import init_logging

__version__ = "0.0.1"
__author__ = "Lukas Calmbach"
__author_email__ = "lcalmbach@gmail.com"
VERSION_DATE = "2023-11-21"
MY_NAME = "Heizungen-BS"
MY_EMOJI = "🏠"
GIT_REPO = "https://github.com/lcalmbach/natural-gase-consumtion-iwb"
LOG_FILE = "./heatings_systems.log"

APP_INFO = f"""<div style="background-color:powderblue; padding: 10px;border-radius: 15px;">
    <small>App created by <a href="mailto:{__author_email__}">{__author__}</a><br>
    version: {__version__} ({VERSION_DATE})<br>
    Datasource: <a href="https://data.bs.ch/">Open Data Basel-Stadt</a><br>
    <a href="{GIT_REPO}">git-repo</a>
    """


def init():
    st.set_page_config(
        layout="centered",
        initial_sidebar_state="auto",
        page_title=MY_NAME,
        page_icon=MY_EMOJI,
    )


def show_info_box():
    """
    Displays an information box in the sidebar with author information, version number, and a link to the git repository.

    Parameters:
    None

    Returns:
    None
    """
    impressum = f"""<div style="background-color:#34282C; padding: 10px;border-radius: 15px; border:solid 1px white;">
    <small>Autoren: <a href="mailto:{__author_email__}">{__author__}</a><br>
    Version: {__version__} ({VERSION_DATE})<br>
    <a href="{GIT_REPO}">git-repo</a>
    """
    st.sidebar.markdown(impressum, unsafe_allow_html=True)


def init_layout():
    """
    Initializes the layout of the application by setting the page configuration, loading CSS styles, and displaying the
    logo in the sidebar.

    Returns:
        None
    """

    def load_css():
        with open("./style.css") as f:
            st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

    st.set_page_config(
        initial_sidebar_state="auto",
        page_title=MY_NAME,
        page_icon=MY_EMOJI,
    )
    load_css()
    st.sidebar.image("./assets/logo.png", width=150)


def main():
    init_layout()
    logger = init_logging(__name__, LOG_FILE)
    logger.info("Starting app...")
    if "app" not in st.session_state:
        st.session_state.app = Buildings()
    app = st.session_state.app = Buildings()
    with st.sidebar:
        st. markdown(f"## {MY_EMOJI} {MY_NAME}")
        # bootstrap icons: https://icons.getbootstrap.com/icons/arrows-angle-contract/
        menu_action = option_menu(
            None,
            app.menu_options,
            icons=app.menu_icons,
            menu_icon="cast",
            default_index=0,
        )
    app.menu_action = menu_action
    show_info_box()


if __name__ == "__main__":
    main()
