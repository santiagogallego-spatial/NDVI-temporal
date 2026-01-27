import os
import sys

# 1. Forzar a que Python use las librerías del entorno virtual antes que las del sistema
venv_path = os.environ.get('VIRTUAL_ENV')
if venv_path:
    # Ruta hacia la base de datos de proyecciones dentro de tu .venv
    proj_db_path = os.path.join(venv_path, 'Lib', 'site-packages', 'rasterio', 'proj_data')
    if not os.path.exists(proj_db_path):
        # A veces está en pyproj si rasterio no la trae
        proj_db_path = os.path.join(venv_path, 'Lib', 'site-packages', 'pyproj', 'proj_data')
    
    os.environ['PROJ_LIB'] = proj_db_path
    # Importante para GDAL (el motor de rasterio)
    os.environ['GDAL_DATA'] = proj_db_path 

import pystac_client
import planetary_computer
import geopandas as gpd
import stackstac
import matplotlib.pyplot as plt
# ... resto del código


import stackstac
import pystac_client
import planetary_computer
import geopandas as gpd
import xarray as xr
import matplotlib.pyplot as plt
import os

# 1. Configuración y Carga de AOI
aoi = gpd.read_file(os.path.join('data/raw', 'study_area.geojson'))

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)

# 2. Búsqueda de todo el año 2023
search = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=aoi.total_bounds,
    datetime="2023-01-01/2023-12-31",
    query={"eo:cloud_cover": {"lt": 5}} # Subimos a 5% para tener más puntos
)

items = search.item_collection()

# 3. Create the Cubo de Datos (Bandas Roja y NIR)
stack = stackstac.stack(
    items, 
    assets=["B04", "B08"], 
    bounds_latlon=aoi.total_bounds,
    epsg=32610
)

# 4. Cálculo de NDVI
# NIR is B08, Red is B04
red = stack.sel(band="B04")
nir = stack.sel(band="B08")

ndvi = (nir - red) / (nir + red)

# 5. Reducir: Promedio espacial por cada fecha
# Esto nos da un valor de NDVI por cada día para toda la parcela
ndvi_mean = ndvi.mean(dim=["x", "y"]).compute()

# 6. Graficar la evolución
plt.figure(figsize=(12, 6))
ndvi_mean.plot(marker='o', color='forestgreen')
plt.title("Temporal Evolution of NDVI - Year 2023 (Madera, CA)")
plt.xlabel("Date")
plt.ylabel("NDVI Average")
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig(os.path.join('outputs', 'ndvi_temporal_2023.png'))
plt.show()

print("✅ Graph generated and saved in the 'outputs' folder")