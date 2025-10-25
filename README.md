# Vélib’ - Where is station capacity most critical?

### Author
**Sean Kamgaing** — EFREI Paris, Data Storytelling 2025

### Project Overview
This dashboard explores **Vélib’ station capacity inequality** across the Paris metropolitan area.  
Using open data from [ParisData / data.gouv.fr](https://www.data.gouv.fr/), it reveals how bike station infrastructure is distributed, highlighting areas with under or over-capacity.

**Key question:**  
- Where is station capacity most critical in the Paris Vélib’ network?

---

### Narrative Flow
1. **Intro :** Context and motivation - importance of equitable access to shared mobility.  
2. **Overview :** Global network metrics, interactive station map, ranking by total capacity.  
3. **Deep Dive :** Distribution of station sizes and variability by commune.  
4. **Conclusions :** Summary insights, correlation analysis, and strategic recommendations.

---

### Dataset
- Source: [Vélib' - Localisation et caractéristique des stations](https://www.data.gouv.fr/datasets/velib-localisation-et-caracteristique-des-stations/)
- Format: CSV
- Variables: station identifier, station name, capacity, coordinates, etc.  
- Period: August 2024 snapshot.

---

### How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
