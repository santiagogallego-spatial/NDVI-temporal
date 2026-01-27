import pystac_client
import planetary_computer
import geopandas as gpd
import os

# 1. Load AOI
aoi = gpd.read_file(os.path.join('data/raw', 'study_area.geojson'))
# We obtain the bounding boxes for the search.
bbox = aoi.total_bounds

# 2. Connect to the Microsoft catalog
catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)

# 3. Define the search
# We will search for Sentinel-2 L2A images (atmospherically corrected)
search = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=bbox,
    datetime="2023-06-01/2023-09-30", # Verano en California (pico vegetativo)
    query={"eo:cloud_cover": {"lt": 10}}, # Menos del 10% de nubes
)

items = search.item_collection()

print(f"✅ They were found. {len(items)} cloud-free images in the selected period.")

# 4. List the dates found to be sure
for item in items:
    print(f"- Image from: {item.datetime.date()} | Cloudiness: {item.properties['eo:cloud_cover']:.2f}%")