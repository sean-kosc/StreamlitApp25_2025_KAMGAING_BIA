import streamlit as st
import plotly.express as px
from utils.viz import hist_capacity, fig_box, COMMUNE_COLORS

def render(tables, filters):
    """Detailed station capacity analysis page"""

    # Filter data if user selected specific communes
    df = tables["stations"]
    if filters["communes"]:
        df = df[df["commune_std"].isin(filters["communes"])]

    # Title and context
    st.title("Detailed analysis - Station capacity patterns")
    st.markdown("""
    This section explores how station capacities are distributed across communes and arrondissements.
    It focuses on variability and concentration to identify areas with either limited or excessive docking capacity.
    """)

    # Histogram of station capacities
    st.markdown("### Distribution of station capacities")
    st.markdown("""
    The histogram below shows how docking capacities are distributed.
    Most stations range between **20 and 35 docks**, with a few very large hubs in central Paris.
    """)

    st.plotly_chart(hist_capacity(df), use_container_width=True)

    # Capacity distribution per commune (box plot)
    st.markdown("### Capacity variability by commune")
    st.markdown("""
    The box plot below compares the capacity range and median for each commune or arrondissement.
    Wider boxes indicate greater variability, while higher medians reveal better-equipped areas.
    """)

    st.plotly_chart(fig_box(df), use_container_width=True)

    # Insight text section
    st.markdown("""
    **Key insight:**  
    Central arrondissements display the highest station capacities, often exceeding 40 docks.
    In contrast, outer communes such as Boulogne-Billancourt, Saint-Denis, or Ivry show smaller
    median capacities, indicating areas where additional infrastructure could be prioritized.
    """)
