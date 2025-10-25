import streamlit as st
import plotly.express as px
from utils.viz import bar_commune, fig_pie_paris_suburbs
import pandas as pd

def render(tables):
    """Introduction page of the Velib dashboard"""

    st.title("Velib Station Network - Île-de-France Overview")

    st.markdown("""
    ### Project goals

    This dashboard provides an analytical overview of Velib stations in the Paris metropolitan area.
    It aims to :
    - Identify where the network capacity is concentrated
    - Highlight differences between Paris arrondissements and suburbs
    - Explore opportunities to rebalance or optimize station distribution
    """)

    # Dataset overview section
    st.markdown("### Dataset overview")

    stats = tables["stats"]
    by_com = tables["by_commune"]
    n = stats["n"]
    q = stats["quantiles"]

    c1, c2, c3 = st.columns(3)
    c1.metric("Total stations", f"{n:,}")
    c2.metric("Median capacity", f"{q[0.5]:.0f}")
    c3.metric("Total capacity (sum)", f"{by_com['capacity_total'].sum():,.0f}")

    st.markdown("""
    **Data source:** [Vélib' - Localisation et caractéristique des stations](https://www.data.gouv.fr/datasets/velib-localisation-et-caracteristique-des-stations/)
    (latest dataset used for this analysis)
    """)

    # Pie chart: Paris vs Suburbs
    st.markdown("### Paris vs Suburbs - Number of Stations")

    df = tables["stations"].copy()
    df["zone"] = df["commune_std"].apply(
        lambda x: "Paris" if "Paris" in str(x) else "Suburbs"
    )
    summary = df.groupby("zone", dropna=False)["id_std"].count().reset_index()
    summary = summary.rename(columns={"id_std": "stations"})

    fig_pie = fig_pie_paris_suburbs(tables["stations"])
    st.plotly_chart(fig_pie, use_container_width=True)

    st.caption("Paris includes all arrondissements, 'Suburbs' refers to the surrounding communes (92, 93, 94, etc.).")

    # Bar chart: Top 10 communes by total capacity
    st.markdown("### Top 10 communes/arrondissements by total capacity")

    fig_bar = bar_commune(by_com, topn=10)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("""
    The ranking highlights that Paris arrondissements dominate the total docking capacity.
    """)

    # Summary section
    st.markdown("""
    ### Next steps

    The following pages will explore:
    - Geographical distribution of stations (Overview),
    - Capacity disparities and density (Detailed Analysis),
    - Interpretation and improvement perspectives (Conclusion).
    """)
