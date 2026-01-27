import geopandas as gpd
from shapely.geometry import Polygon
import os

# 1. Define the coordinates of the irregular polygon (Longitude, Latitude)
# It is an agricultural sector in Madera County, California.
coords = [
    [-120.360, 37.080], # North-west corner
    [-120.320, 37.080], # Follows a road line
    [-120.320, 37.095], # Climb up a lot division
    [-120.290, 37.095], # Extend east
    [-120.290, 37.060], # Descend following a canal
    [-120.330, 37.060], # Cut west
    [-120.330, 37.045], # Descend a little further
    [-120.360, 37.045], # Closes the southern block
    [-120.360, 37.080]  # Total closure
]

# 2. Create the geometry and GeoDataFrame
poly = Polygon(coords)
gdf = gpd.GeoDataFrame(index=[0], crs='EPSG:4326', geometry=[poly])
gdf['name'] = 'Sector_Madera_CA'

# 3. Define the path and save
output_path = os.path.join('data/raw', 'study_area.geojson')

# Create the data folder if it does not exist
if not os.path.exists('data/raw'):
    os.makedirs('data/raw')

gdf.to_file(output_path, driver='GeoJSON')

print(f"✅ File successfully created in: {output_path}")