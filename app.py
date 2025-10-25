import streamlit as st
from utils.io import load_data, LOCAL_PATH
from utils.prep import normalize
from sections import intro, overview, deep_dives, conclusions
from pathlib import Path
import plotly.express as px
from PIL import Image

# --- CONFIG PAGE ---
st.set_page_config(page_title="Vélib’ - Station capacities", layout="wide")

# --- LOADING ---
@st.cache_data(show_spinner=False)
def get_tables(file_mtime: float, arr_mtime: float, com_mtime: float):
    """Returns normalized tables. Cache depends on CSV timestamp."""
    df_raw = load_data()
    return normalize(df_raw)

# --- TITRE ---
logo = Image.open(Path(__file__).resolve().parent / "assets" / "velib_logo.png")
col1, col2 = st.columns([0.1, 0.9])  # smaller column for the logo
with col1:
    st.image(logo, width=70)
with col2:
    st.title("Vélib’ - Where is station capacity most critical?")
st.caption("Source : ParisData / data.gouv — Vélib’ Localisation & caractéristiques des stations.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Filters")

    try:
        file_mtime = LOCAL_PATH.stat().st_mtime
    except Exception:
        file_mtime = 0

    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    arr_path = data_dir / "arrondissements.geojson"
    com_path = data_dir / "communes-version-simplifiee.geojson"

    try:
        file_mtime = LOCAL_PATH.stat().st_mtime
    except Exception:
        file_mtime = 0

    arr_mtime = arr_path.stat().st_mtime if arr_path.exists() else 0
    com_mtime = com_path.stat().st_mtime if com_path.exists() else 0

    tables = get_tables(file_mtime, arr_mtime, com_mtime)

    from utils.viz import set_commune_colors
    communes = tables["by_commune"]["commune_std"].unique()
    set_commune_colors(communes)

    communes_all = tables["stations"]["commune_std"].dropna().unique().tolist()
    show_commune_filter = [c for c in communes_all if c and c != "(Inconnu)"]
    if show_commune_filter:
        communes_sel = st.multiselect("Commune / Arrondissement", sorted(show_commune_filter), default=[])
    else:
        with st.expander("Aperçu de 'by_commune' (debug)"):
            st.write(tables.get("by_commune"))
        communes_sel = []

    page = st.radio(
        "Sections",
        ["Intro", "Overview", "Detailed analysis", "Conclusions"]
    )
    filters = {"communes": communes_sel}

if page == "Intro":
    intro.render(tables)
elif page == "Overview":
    overview.render(tables, filters)
elif page == "Detailed analysis":
    deep_dives.render(tables, filters)
else:
    conclusions.render(tables)
