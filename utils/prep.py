import pandas as pd
import numpy as np
import unicodedata
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path
import re


def _format_arr_label(l_ar: str) -> str:
    """'10ème Ardt' -> 'Paris - 10e arrondissement'  |  '1er Ardt' -> 'Paris - 1er arrondissement'"""
    if not isinstance(l_ar, str):
        return None
    m = re.search(r"(\d+)", l_ar)
    if not m:
        return None
    n = int(m.group(1))
    suffix = "er" if n == 1 else "e"
    return f"Paris - {n}{suffix} arrondissement"

def assign_commune_geojson(df):
    base_dir = Path(__file__).resolve().parents[1]
    path_arr = base_dir / "data" / "arrondissements.geojson"
    path_com = base_dir / "data" / "communes-version-simplifiee.geojson"

    # Load districts and KEEP only the ar
    gdf_arr = gpd.read_file(path_arr).to_crs("EPSG:4326")
    if "l_ar" not in gdf_arr.columns:
        raise ValueError("Le GeoJSON d'arrondissements doit contenir 'l_ar'.")
    gdf_arr = gdf_arr[["l_ar", "geometry"]].copy()
    gdf_arr["arrondissement_nom"] = gdf_arr["l_ar"].apply(_format_arr_label)

    # Charging municipalities
    gdf_com = gpd.read_file(path_com).to_crs("EPSG:4326")
    gdf_com = gdf_com[["nom", "geometry"]].rename(columns={"nom": "commune_nom"})

    # Vélib -> GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df.copy(),
        geometry=gpd.points_from_xy(df["lon"], df["lat"]),
        crs="EPSG:4326",
    )

    # Spatial join (boroughs first)
    gdf = gpd.sjoin(
        gdf,
        gdf_arr[["arrondissement_nom", "geometry"]],
        how="left",
        predicate="within",
    ).drop(columns=["index_right"], errors="ignore")

    # Spatial joint (communes)
    gdf = gpd.sjoin(
        gdf,
        gdf_com[["commune_nom", "geometry"]],
        how="left",
        predicate="within",
    ).drop(columns=["index_right"], errors="ignore")

    gdf["commune_std"] = gdf["arrondissement_nom"].where(
        gdf["arrondissement_nom"].notna(), gdf["commune_nom"]
    ).fillna("(Inconnu)")

    gdf = gdf.drop(columns=[c for c in gdf.columns if c in {"l_ar", "l_aroff"}], errors="ignore")
    gdf = gdf.drop(columns=["geometry"], errors="ignore")

    return pd.DataFrame(gdf)


def _norm(s: str) -> str:
    if s is None:
        return ""
    s = str(s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s.lower()


def _find_column(df: pd.DataFrame, keywords: list):
    norm_map = {col: _norm(col) for col in df.columns}
    for col, normcol in norm_map.items():
        tokens = normcol.split()
        for kw in keywords:
            if kw in tokens:
                return col
    for col, normcol in norm_map.items():
        for kw in keywords:
            if kw in normcol:
                return col
    return None

def normalize(df: pd.DataFrame):
    """
    Normalizes the Vélib file downloaded from data.gouv.fr
    (Station identifier, Station name, Station capacity, Geographic coordinates).
    """
    col_id = _find_column(df, ["identifiant", "id"] ) or "Identifiant station"
    col_name = _find_column(df, ["nom", "name"]) or "Nom de la station"
    col_cap = _find_column(df, ["capacit", "capacity", "capacite"]) or "Capacité de la station"
    col_geo = _find_column(df, ["coord", "geograph", "latitude", "longitude"]) or "Coordonnées géographiques"

    if col_geo in df.columns:
        parts = (
            df[col_geo]
            .astype(str)
            .str.replace(r"[\(\)\[\]]", "", regex=True)
            .str.split(",", n=1, expand=True)
        )
        df["lat"] = pd.to_numeric(parts[0].str.strip(), errors="coerce")
        df["lon"] = pd.to_numeric(parts[1].str.strip(), errors="coerce")
    else:
        df["lat"], df["lon"] = np.nan, np.nan

    if col_cap in df.columns:
        df["capacity_std"] = pd.to_numeric(df[col_cap], errors="coerce")
    else:
        df["capacity_std"] = pd.NA

    df["id_std"] = df[col_id] if col_id in df.columns else pd.NA
    df["name_std"] = df[col_name] if col_name in df.columns else pd.NA

    df = assign_commune_geojson(df)

    core = df[["id_std", "name_std", "commune_std", "capacity_std", "lat", "lon"]].copy()
    core = core.dropna(subset=["lat", "lon"])
    core = core[core["capacity_std"].notna()]

    if not core.empty:
        by_com = (
            core.groupby("commune_std", dropna=False)
            .agg(
                stations=("id_std", "count"),
                capacity_total=("capacity_std", "sum"),
                capacity_median=("capacity_std", "median"),
            )
            .reset_index()
            .sort_values("capacity_total", ascending=False)
        )
        q = core["capacity_std"].quantile([0.1, 0.25, 0.5, 0.75, 0.9]).to_dict()
    else:
        by_com = pd.DataFrame(columns=["commune_std", "stations", "capacity_total", "capacity_median"])
        q = {}

    return {
        "stations": core,
        "by_commune": by_com,
        "stats": {"quantiles": q, "n": len(core)},
    }
