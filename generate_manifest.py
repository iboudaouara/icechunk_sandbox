import os
import xarray as xr
import icechunk

zarr_source = "gdps_2026031800.zarr"
repo_path = "my_icechunk_repo"

if not os.path.exists(zarr_source):
    print(f"Erreur : {zarr_source} n'existe pas.")
    exit()

# 1. Ouvrir sans chercher la consolidation (évite le warning)
ds = xr.open_zarr(zarr_source, consolidated=False)

# 2. Configuration du stockage du REPO
storage = icechunk.local_filesystem_storage(repo_path)

# 3. Configuration du dépôt
config = icechunk.RepositoryConfig.default()

# 4. Correction de la VirtualChunkContainer
# Note l'utilisation de .local_filesystem_store (avec un 'e') pour le 2ème argument
config.set_virtual_chunk_container(
    icechunk.VirtualChunkContainer(
        f"file://{os.path.abspath(zarr_source)}/", # Utiliser le chemin absolu est plus sûr
        icechunk.local_filesystem_store(zarr_source)
    )
)

# 5. Création ou Ouverture
if not os.path.exists(repo_path) or not os.listdir(repo_path):
    repo = icechunk.Repository.create(storage, config)
    print(f"Dépôt Icechunk créé dans : {repo_path}")
else:
    repo = icechunk.Repository.open(storage)
    print("Dépôt Icechunk ouvert")
try:
    # On essaie de lister les snapshots de la branche 'main'
    snapshots = list(repo.ancestry("main"))
except Exception:
    # Si la branche n'existe pas encore (premier run), la liste est vide
    snapshots = []

if snapshots:
    print(f"Snapshot trouvé : {snapshots[0]}. Skipping commit.")
else:
    # On crée une session d'écriture
    session = repo.writable_session("main")

    # On écrit les métadonnées (Virtual Chunks)
    ds.to_zarr(session.store, mode="w")

    # On commit et on récupère le snapshot_id
    snapshot_id = session.commit("Import GDPS via Virtual Chunks")
    print(f"Commit réussi ! ID: {snapshot_id}")


**How it is handled:**

| Feature | Zarr v2 (The Workaround) | Zarr v3 (The Standard) |
| :--- | :--- | :--- |
| **Format** | Scattered `.zarray`, `.zgroup`, `.zattrs` files. | Unified `zarr.json` files. |
| **Consolidation** | Opt-in patch (`.zmetadata`). | Natively integrated via extensions. |
| **Usage** | Requires explicit functions (e.g., `zarr.open_consolidated()`). | Transparent. Clients handle it automatically. |
| **Maintenance** | Manual updates required when dataset structure changes. | Standardized and inherently managed. |
