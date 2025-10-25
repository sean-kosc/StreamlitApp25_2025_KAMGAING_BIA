import streamlit as st
from utils.viz import fig_pie_capacity_share, fig_scatter_capacity_vs_stations

def render(tables):
    """
    Final conclusions page of the Velib capacity analysis dashboard.
    Summarizes results, provides key insights, and presents strategic recommendations.
    """

    # ----- Page Title -----
    st.title("Conclusions and Strategic Insights")
    st.markdown("""
    This section consolidates the key results of the analysis and offers recommendations
    for improving the balance and accessibility of the Vélib’ network across the Paris region.
    """)

    # ----- Load and compute global statistics -----
    df = tables["stations"]
    df_by_commune = tables["by_commune"]

    total_capacity = int(df["capacity_std"].sum())
    avg_capacity = round(df["capacity_std"].mean(), 1)
    top_commune = df_by_commune.loc[df_by_commune["capacity_total"].idxmax(), "commune_std"]

    st.markdown(f"""
    **Key figures:**
    - Total docking capacity: **{total_capacity:,}**
    - Average station capacity: **{avg_capacity}**
    - Commune with the highest total capacity: **{top_commune}**
    """)

    # ----- Pie chart: Distribution of capacity -----
    st.subheader("Network share by commune")
    st.markdown("""
    The following pie chart illustrates how total docking capacity is distributed
    between communes. Paris arrondissements clearly dominate the network’s total capacity,
    highlighting a long-standing infrastructure concentration in central areas.
    """)

    fig = fig_pie_capacity_share(df_by_commune)
    st.plotly_chart(fig, use_container_width=True)

    # ----- Analytical correlation: stations vs capacity -----
    st.subheader("Correlation between number of stations and total capacity")
    st.markdown("""
    The scatter plot below explores the relationship between the number of stations
    in each commune and their combined docking capacity. The strong positive correlation
    indicates that larger station counts directly scale with overall capacity.
    However, outer communes display smaller capacities even with similar station counts,
    reflecting infrastructure under-sizing relative to potential demand.
    """)

    fig2 = fig_scatter_capacity_vs_stations(df_by_commune)
    st.plotly_chart(fig2, use_container_width=True)

    # ----- Summary -----
    st.markdown("""
    ### Summary of insights
    - Paris intramuros holds most of the network’s docking infrastructure.
    - Outer communes such as Boulogne-Billancourt, Saint-Denis, and Ivry remain under-equipped.
    - Median station sizes are consistent, showing uniform installation standards.
    - However, accessibility asymmetry persists between central and peripheral zones.
    """)

    # ----- Strategic recommendations -----
    st.markdown("### Recommendations for city planners")
    st.markdown("""
    - **Redistribute future installations** to communes with low station density and limited total capacity.
    - **Increase docking capacity** in high-demand zones such as intermodal transport hubs.
    - **Integrate temporal data** (like rush hours, weather, events) to dynamically optimize bike availability.
    - **Adopt predictive analytics** for long-term demand forecasting and fair infrastructure allocation.
    """)

    # ----- Closing message -----
    st.markdown("""
    In summary, the Vélib’ system forms a solid backbone for sustainable urban mobility.
    Nevertheless, to ensure equitable accessibility and long-term resilience,
    targeted infrastructure adjustments are required across the Paris metropolitan area.
    """)
