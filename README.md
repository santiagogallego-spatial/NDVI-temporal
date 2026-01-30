# 🛰️ Agri-Intelligence Spatial Correlation: Hamilton, IA
### **Predictive Biophysical Modeling: Sentinel-2 & ERA5-Land Integration**

---

## 🚀 Strategic Value Proposition
Understanding crop performance requires more than just looking at a green map. This engine synchronizes **Sentinel-2 Multispectral Data (10m)** with **ERA5-Land Soil Moisture (9km)** to quantify the biological efficiency of a field. By measuring the "Mirror Effect" between vegetation vigor and water depletion, we provide a high-resolution diagnostic of crop health and resilience.

**Key Business Benefits:**
* **Resource Optimization:** Identify exactly which areas of a lot are most sensitive to water stress.
* **Resilience Validation:** Scientifically prove if a crop is effectively utilizing soil moisture during peak summer (Evapotranspiration monitoring).
* **Data-Driven Auditing:** High-precision metrics ($R^2$, $p$-value) to back up management decisions before stakeholders.

---

## 📊 Analytical Deliverables & Insights

### 1. Spatial Sensitivity Map (Pearson r)
A high-resolution raster (10m/pixel) using a **Pearson Correlation engine**. It identifies the "Water-Usage Zones" where vegetation growth is most synchronized with soil moisture availability.

<p align="center">
  <img src="outputs/spatial_correlation_map.png" width="600" title="Spatial Correlation Map">
</p>



### 2. Biophysical Regression (NDVI vs. Moisture)
We don't just show correlations; we prove them. This scatter plot demonstrates the inverse relationship during the peak growing season, validating that biomass increase is driving soil water consumption.

<p align="center">
  <img src="outputs/scatter_correlation.png" width="600" title="Scatter Correlation Plot">
</p>



> **Key Insight:** Our 2023 model achieved a **Pearson $r$ of -0.915**, indicating that 83.7% of the crop's vigor is directly explained by active water transpiration dynamics.

### 3. Automated Executive Reporting
A "ready-to-present" PDF report generated automatically, summarizing methodology, statistical precision, and management recommendations.

---

## 🛠️ Technical Workflow & Criteria
The system processes millions of pixels using a **Time-Series Alignment** method to match satellite irregular captures with monthly climate reanalysis.

| Variable | Source | Rationale |
| :--- | :--- | :--- |
| **NDVI** | Sentinel-2 L2A | Primary proxy for photosynthetic activity and biomass. |
| **Soil Moisture** | ERA5-Land (swvl1) | Volumetric water content in the topsoil (0-7cm). |
| **Temporal Resampling**| 1-Month Step | Aligns disparate data sources for robust statistical comparison. |
| **Seasonal Filtering** | Apr - Oct | Focuses analysis on the active phenological cycle. |

---

## 💻 Software Architecture
This is a **productized pipeline** built for scalability and low-resource consumption by using local data cubes (`.nc`).

```text
NDVI_temporal/
│
├─ scripts/                 # Source code (Serialized execution)
│   ├─ 03_ndvi_temporal.py  # Ingests API data & creates local NetCDF cube
│   ├─ 07_pearson_map.py    # Spatial downscaling & pixel-level correlation
│   ├─ 08_statistics.py     # Scipy engine for R2 and P-Value validation
│   └─ 09_generate_pdf.py   # Automated English Professional Reporting
│
├─ data/                    # Datasets (ERA5 & Shapefiles)
│   └─ clima_historico_10y.nc
│
├─ outputs/                 # Results & Artifacts
│   ├─ ndvi_cube_2023.nc    # Serialized satellite data cube
│   ├─ spatial_correlation_map.png
│   ├─ scatter_correlation.png
│   └─ Final_Report_Hamilton_Professional.pdf
│
├─ README.md
├─ requirements.txt  
└─ .gitignore

---

## 👨‍💻 Author & Consultancy
**Santiago Gallego** Agronomist Engineer | Geospatial Software Developer I bridge the gap between **Agronomy**, **Data Science**, and **GIS** to provide actionable intelligence for the AgTech sector.

