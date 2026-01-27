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


import pystac_client
import planetary_computer
import geopandas as gpd
import stackstac
import matplotlib.pyplot as plt
import os

# 1. Load AOI
aoi = gpd.read_file(os.path.join('data/raw', 'study_area.geojson'))

# 2. Connection and Search (We copy the above, but only the best image)
catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)

search = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=aoi.total_bounds,
    datetime="2023-09-01/2023-09-30",
    query={"eo:cloud_cover": {"lt": 1}}
)

items = search.item_collection()
# We take the first one (the most recent one from the search engine).
item = items[0]

# 3. Load True Color bands (Red, Green, Blue)
# stackstac does the magic of cropping only our AOI
stack = stackstac.stack(
    item, 
    assets=["B04", "B03", "B02"], 
    bounds_latlon=aoi.total_bounds,
    epsg=32610 
)
# 4. Convert to real image (numpy) and plot
# Note: We divide by 10,000 because Sentinel stores values as integers.
data = stack.compute()
rgb = data.squeeze().values / 10000 

# Reorder axes so that matplotlib understands them (Bands, Height, Width -> Height, Width, Bands)
rgb_fixed = rgb.transpose(1, 2, 0)

#5. Show results
plt.figure(figsize=(10, 10))
plt.imshow(rgb_fixed.clip(0, 0.3) / 0.3) # Ajuste de brillo básico
plt.title(f"True Color Image - {item.datetime.date()}")
plt.axis('off')
plt.show()

