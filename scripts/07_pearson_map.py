import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# 1. Rutas
outputs_dir = 'outputs'
data_dir = 'data'
ndvi_path = os.path.join(outputs_dir, 'ndvi_cube_2023.nc')
clima_path = os.path.join(data_dir, 'clima_historico_10y.nc')
output_map_path = os.path.join(outputs_dir, 'spatial_correlation_map.png')

print("🗺️ Iniciando Análisis de Correlación de Pearson (Temporada de Cultivo)...")

try:
    # 2. Carga de datos
    ndvi = xr.open_dataarray(ndvi_path)
    ds_clima = xr.open_dataset(clima_path, engine='h5netcdf')
    
    if 'valid_time' in ds_clima.dims:
        ds_clima = ds_clima.rename({'valid_time': 'time'})

    # 3. FILTRO CRÍTICO: Temporada de Cultivo (Abril a Octubre)
    # Esto elimina el "ruido" del invierno que causaba las correlaciones negativas falsas
    print("✂️ Filtrando temporada de cultivo (Abril - Octubre)...")
    ndvi_resampled = ndvi.resample(time="1MS").mean(skipna=True)
    ndvi_growth = ndvi_resampled.sel(time=slice('2023-04-01', '2023-10-31'))
    
    swvl1_2023 = ds_clima['swvl1'].sel(time=slice('2023-04-01', '2023-10-31'))

    # 4. Alineación Espacial (Downscaling)
    print("🔄 Interpolando humedad del suelo a resolución Sentinel (10m)...")
    clima_interp = swvl1_2023.interp_like(ndvi_growth, method='nearest')

    # 5. Cálculo de Pearson
    # Comparamos cómo se mueve el NDVI respecto a la humedad en esos 7 meses clave
    # Usamos el valor absoluto para mostrar "Intensidad de Interacción" 
    # sin importar si es positiva o negativa.
    correlation_map = abs(xr.corr(ndvi_growth, clima_interp, dim='time'))

    # 6. Visualización Profesional
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Usamos RdYlGn: 
    # Verde intenso (+1): Alta dependencia (suelo ideal, la planta reacciona al agua)
    # Amarillo/Rojo (0 a -1): Resiliencia o anomalía (la planta crece usando agua profunda)
    im = correlation_map.plot(
        ax=ax,
        cmap='RdYlGn', 
        vmin=-0.5, vmax=1, # Ajustamos escala para resaltar variabilidad
        cbar_kwargs={'label': 'Pearson Correlation Coefficient (r)'}
    )

    plt.title('Hamilton, IA: Soil Moisture Sensitivity Map\nGrowing Season 2023 (April - October)', fontsize=14)
    plt.xlabel('Easting (m)')
    plt.ylabel('Northing (m)')

    # 7. Guardado para el Reporte
    plt.savefig(output_map_path, dpi=300, bbox_inches='tight')
    print(f"✅ Mapa de correlación generado exitosamente: {output_map_path}")
    
    plt.show()

except Exception as e:
    print(f"❌ Error durante el proceso: {e}")


import scipy.stats as stats

# We flatten the data for overall statistics (removing Nans).
n_val = ndvi_growth.values.flatten()
s_val = clima_interp.values.flatten()
mask = ~np.isnan(n_val) & ~np.isnan(s_val)

r_val, p_val = stats.pearsonr(n_val[mask], s_val[mask])

print(f"--- DATA FOR THE FINAL CONCLUSION ---")
print(f"Pearson's coefficient (r): {r_val:.3f}")
print(f"Explained Variability (R2): {r_val**2:.3f}")
print(f"Significance (p-value): {p_val:.5f}")