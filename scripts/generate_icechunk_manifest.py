import os
import xarray as xr
import icechunk

vds = xr.open_zarr("alberta_region.zarr")

storage = icechunk.local_filesystem_storage("oisst")

# repo config
config = icechunk.RepositoryConfig.default()
config.set_virtual_chunk_container(
    icechunk.VirtualChunkContainer(
        "file://alberta_region.zarr/",
        icechunk.local_filesystem_store("alberta_region.zarr")
    )
)

# 👇 clé : create OU open
if not os.path.exists(repo_path) or not os.listdir(repo_path):
    repo = icechunk.Repository.create(storage, config)
    print("Repo created")
else:
    repo = icechunk.Repository.open(storage)
    print("Repo opened")

snapshots = repo.list_snapshots()

if snapshots:
    # tu peux comparer metadata ou hash
    print("Snapshot exists, skipping commit")
else:
    session = repo.writable_session("main")
    vds.to_zarr(session.store, mode="w")
    snapshot_id = session.commit("import alberta region dataset")
    print(snapshot_id)

print(vds)
print(snapshots)
