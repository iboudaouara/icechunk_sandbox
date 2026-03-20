import xarray as xr
import numpy as np
import pandas as pd

# 1. Définir les dimensions
# Création de 10 jours de données, pour une grille globale (1 degré de résolution)
times = pd.date_range("2026-01-01", periods=10, freq="D")
lats = np.arange(-90, 91, 1)   # De -90 à +90
lons = np.arange(-180, 180, 1) # De -180 à +179

# 2. Générer des données numériques factices (Température de l'air)
# La forme du tableau doit correspondre à (time, lat, lon) -> (10, 181, 360)
# Générons des températures aléatoires entre -20°C et 40°C
temperature_data = np.random.uniform(low=-20, high=40, size=(len(times), len(lats), len(lons)))

# 3. Créer le Dataset Xarray
ds = xr.Dataset(
    data_vars={
        "air_temperature": (["time", "lat", "lon"], temperature_data, {"units": "Celsius"})
    },
    coords={
        "time": times,
        "lat": (["lat"], lats, {"units": "degrees_north"}),
        "lon": (["lon"], lons, {"units": "degrees_east"}),
    },
    attrs={
        "description": "Données synthétiques de température de l'air pour test Zarr",
        "author": "Ibrahim"
    }
)

# 4. Optimiser avec des "Chunks" (Morceaux)
# C'est la force de Zarr ! On divise les données en petits blocs pour une lecture rapide.
ds = ds.chunk({
    "time": 5,    # 5 jours par morceau
    "lat": 90,    # 90 degrés de latitude par morceau
    "lon": 90     # 90 degrés de longitude par morceau
})

# 5. Sauvegarder en Zarr
zarr_path = "temperature_data.zarr"
ds.to_zarr(zarr_path, mode="w")

print(f"✅ Fichier Zarr créé avec succès : {zarr_path}")
print(ds)
