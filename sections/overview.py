import streamlit as st
import plotly.express as px
from utils.viz import map_chart, bar_commune, COMMUNE_COLORS

def render(tables, filters):
    """Overview page showing general network patterns"""

    # Data filtering based on selected communes
    df = tables["stations"]
    if filters["communes"]:
        df = df[df["commune_std"].isin(filters["communes"])]

    # Key metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Stations", f"{df.shape[0]:,}")
    c2.metric("Total capacity", f"{int(df['capacity_std'].sum()):,}")
    c3.metric("Median capacity", f"{int(df['capacity_std'].median()) if len(df) else 0}")
    low_thr = tables["stats"]["quantiles"].get(0.1, None)
    c4.metric("Stations below 10th percentile", f"{int((df['capacity_std'] < low_thr).sum()) if low_thr else 0:,}")

    # Section introduction
    st.markdown("### Network overview")
    st.markdown("""
    This section provides a general view of the Velib network across the Paris region.
    It highlights how docking capacity is distributed and identifies areas with higher density.
    """)

    # Interactive map
    st.subheader("Station map")
    st.markdown("""
    Each point represents a station, colored by its commune or arrondissement.
    Larger clusters of points indicate higher local density.
    """)
    st.plotly_chart(map_chart(df), use_container_width=True)

    # Capacity distribution chart
    st.markdown("### Capacity distribution across communes")
    st.markdown("""
    This bar chart compares the total docking capacity between communes.
    It reveals where the largest portions of the network are concentrated.
    """)

    df_communes = tables["by_commune"].sort_values("capacity_total", ascending=False)

    fig = px.bar(
        df_communes,
        x="commune_std",
        y="capacity_total",
        text_auto=".2s",
        color="commune_std",
        color_discrete_map=COMMUNE_COLORS,
        hover_name="commune_std",
        hover_data={"capacity_total": True}
    )

    # Improved visual spacing for readability
    fig.update_layout(
        xaxis_title="Commune or arrondissement",
        yaxis_title="Total docking capacity",
        showlegend=False,
        bargap=0.35,  # increased spacing for better readability
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
    )
    fig.update_traces(marker_line_width=0.5, marker_line_color="rgba(255,255,255,0.3)")

    st.plotly_chart(fig, use_container_width=True)

    # Commentary section
    st.markdown("""
    Paris arrondissements display the highest overall capacity, which reflects the historical
    and infrastructural concentration of the Velib network within the city center.
    However, suburban communes such as Boulogne-Billancourt, Montreuil, and Saint-Denis
    have developed dense station networks as well, supporting strong local demand.
    """)

    # Add a compact summary below
    st.markdown("""
    **Key insight:**  
    The capacity distribution remains highly centralized, indicating potential
    for further expansion in outer communes to balance accessibility.
    """)
