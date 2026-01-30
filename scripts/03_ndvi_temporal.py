import os
import sys

# 1. Tu bloque original de configuración de PROJ (el que te funcionaba)
venv_path = os.environ.get('VIRTUAL_ENV')
if venv_path:
    proj_db_path = os.path.join(venv_path, 'Lib', 'site-packages', 'rasterio', 'proj_data')
    if not os.path.exists(proj_db_path):
        proj_db_path = os.path.join(venv_path, 'Lib', 'site-packages', 'pyproj', 'proj_data')
    
    os.environ['PROJ_LIB'] = proj_db_path
    os.environ['GDAL_DATA'] = proj_db_path 

import pystac_client
import planetary_computer
import geopandas as gpd
import stackstac
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd # Añadido para exportar

# 2. Carga de AOI (Usando tu ruta original)
aoi = gpd.read_file(os.path.join('data/raw', 'study_area.geojson'))

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)

# 3. Búsqueda
search = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=aoi.total_bounds,
    datetime="2023-01-01/2023-12-31",
    query={"eo:cloud_cover": {"lt": 5}}
)

items = search.item_collection()
print(f"✅ Found {len(items)} items.")

# 4. Cubo de Datos (Mantengo tu EPSG original 32610)
stack = stackstac.stack(
    items, 
    assets=["B04", "B08"], 
    bounds_latlon=aoi.total_bounds,
    epsg=32610
)

# 5. Cálculo de NDVI
red = stack.sel(band="B04")
nir = stack.sel(band="B08")
ndvi = (nir - red) / (nir + red)

# 6. Reducción espacial
print("🧪 Computing NDVI mean...")
ndvi_mean = ndvi.mean(dim=["x", "y"]).compute()

# --- NUEVA SECCIÓN: EXPORTACIÓN DE DATOS ---
# Convertimos el resultado a un DataFrame para el script de correlación
df_stats = ndvi_mean.to_dataframe(name='ndvi_mean').reset_index()

# Limpiamos valores nulos y renombramos 'time' a 'date' para que el script 06 lo entienda
df_stats = df_stats.dropna(subset=['ndvi_mean'])
df_stats = df_stats.rename(columns={'time': 'date'})

# Guardamos el CSV en la carpeta outputs
os.makedirs('outputs', exist_ok=True)
csv_path = os.path.join('outputs', 'ndvi_stats.csv')
df_stats.to_csv(csv_path, index=False)
print(f"📊 Stats saved to: {csv_path}")
# -------------------------------------------

# 7. Graficar
plt.figure(figsize=(12, 6))
ndvi_mean.plot(marker='o', color='forestgreen')
plt.title("Temporal Evolution of NDVI - Year 2023")
plt.xlabel("Date")
plt.ylabel("NDVI Average")
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig(os.path.join('outputs', 'ndvi_temporal_2023.png'))
plt.show()

print("✅ Graph generated and saved in the 'outputs' folder")

# 1. Creamos una copia limpia para exportar
# Eliminamos las coordenadas que empiezan con 'proj:' o 'raster:' que causan el error
coords_to_drop = [c for c in ndvi.coords if ':' in str(c)]
ndvi_export = ndvi.drop_vars(coords_to_drop)

# 2. Eliminamos todos los atributos (metadata técnica)
ndvi_export.attrs = {}

# 3. Guardar el cubo limpio
ndvi_cube_path = os.path.join('outputs', 'ndvi_cube_2023.nc')
print("💾 Serializando cubo NDVI a NetCDF...")
ndvi_export.to_netcdf(ndvi_cube_path)

print(f"✅ Cubo guardado exitosamente en: {ndvi_cube_path}")