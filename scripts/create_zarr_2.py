import xarray as xr
import numpy as np
import pandas as pd

version = 3

run_time = pd.Timestamp.now(tz="UTC").floor("D").tz_localize(None)

times = pd.date_range(run_time, periods=48, freq="1h")
lats = np.arange(-90, 91, 1)   
lons = np.arange(0, 360, 1)

temperature_data = np.random.uniform(low=-20, high=40, size=(len(times), len(lats), len(lons)))

ds = xr.Dataset(
    data_vars={
        "TT": (["time", "lat", "lon"], temperature_data, {"units": "Celsius"})
    },
    coords={
        "time": times,
        "lat": (["lat"], lats, {"units": "degrees_north"}),
        "lon": (["lon"], lons, {"units": "degrees_east"}),
    },
    attrs={
        "description": "Prévisions factices GDPS",
        "model": "Global Deterministic Prediction System (GDPS) mock",
        "author": "Ibrahim"
    }
)

# 4. Optimiser avec des "Chunks"
ds = ds.chunk({
    "time": 5,    
    "lat": 90,    
    "lon": 90     
})

# 5. Formater le nom du fichier à la manière du CMC (ex: gdps_2026031800.zarr)
timestamp_str = run_time.strftime("%Y%m%d%H")
zarr_path = f"gdps_{timestamp_str}_v{version}.zarr"

# 6. Sauvegarder en Zarr v3 (sans consolidation pour éviter le warning)
ds.to_zarr(
    zarr_path, 
    mode="w", 
    zarr_format=version, 
    consolidated=False
)

print(f"✅ Fichier Zarr v3 créé avec succès : {zarr_path}")
