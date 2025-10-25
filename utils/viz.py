import plotly.express as px

COMMUNE_COLORS = {}
def set_commune_colors(communes):
    """
    Defines the common palette for all Plotly figures.
    It generates a {common: color} dictionary.
    """
    global COMMUNE_COLORS
    palette = px.colors.qualitative.Safe
    COMMUNE_COLORS = {
        com: palette[i % len(palette)] for i, com in enumerate(communes)
    }

def map_chart(df):
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        color="commune_std",
        hover_name="name_std",
        hover_data={"commune_std": True, "capacity_std": True, "lat": False, "lon": False},
        zoom=10,
        height=520,
        color_discrete_map=COMMUNE_COLORS
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(
            title="Commune / Arrondissement",
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(0,0,0,0.5)",
            font=dict(size=12, color="white")
        )
    )
    return fig


def bar_commune(df_commune, topn=None):
    d = df_commune.copy()
    if topn:
        d = d.head(topn)
    fig = px.bar(
        d,
        x="commune_std",
        y="capacity_total",
        color="commune_std",
        text_auto=".2s",
        color_discrete_map=COMMUNE_COLORS
    )
    fig.update_layout(
        xaxis_title="Commune",
        yaxis_title="Total capacity",
        showlegend=False,
        bargap=0.25,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    return fig


def hist_capacity(df):
    fig = px.histogram(df, x="capacity_std", nbins=30, opacity=0.8)
    fig.update_traces(marker_line_width=1, marker_line_color="white")
    fig.update_layout(xaxis_title="Station capacity", yaxis_title="Count", bargap=0.15)
    return fig

def fig_box(df):
    fig = px.box(
        df,
        x="commune_std",
        y="capacity_std",
        color="commune_std",
        color_discrete_map=COMMUNE_COLORS,
        title="Capacity distribution across communes",
        points="all",
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title="Commune or arrondissement",
        yaxis_title="Docking capacity",
        bargap=0.4,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
    )
    return fig

def fig_pie_paris_suburbs(df):
    """
    Returns a pie chart showing the proportion of Velib stations in Paris vs Suburbs.
    """
    import plotly.express as px

    # Determine whether a station is in Paris or in the suburbs
    df = df.copy()
    df["zone"] = df["commune_std"].apply(
        lambda x: "Paris" if "Paris" in str(x) else "Suburbs"
    )

    # Count number of stations by zone
    summary = df.groupby("zone", dropna=False)["id_std"].count().reset_index()
    summary = summary.rename(columns={"id_std": "stations"})

    # Create the pie chart
    fig = px.pie(
        summary,
        names="zone",
        values="stations",
        title="Distribution of stations: Paris vs Suburbs",
        color_discrete_sequence=px.colors.qualitative.Safe,
    )
    fig.update_traces(textinfo="percent+label", textfont_size=14)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
    )
    return fig

def fig_pie_capacity_share(df_by_commune):
    """
    Returns a pie chart showing each commune's share of total docking capacity.
    Used in the Conclusions page.
    """
    import plotly.express as px
    from utils.viz import COMMUNE_COLORS

    fig = px.pie(
        df_by_commune,
        names="commune_std",
        values="capacity_total",
        color="commune_std",
        color_discrete_map=COMMUNE_COLORS,
        title="Share of total capacity by commune",
    )
    fig.update_traces(textinfo="percent+label", pull=[0.02] * len(df_by_commune))
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
    )
    return fig

def fig_scatter_capacity_vs_stations(df_by_commune):
    import plotly.express as px
    fig = px.scatter(
        df_by_commune,
        x="stations",
        y="capacity_total",
        color="commune_std",
        size="capacity_median",
        color_discrete_map=COMMUNE_COLORS,
        title="Correlation between number of stations and total capacity",
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    return fig