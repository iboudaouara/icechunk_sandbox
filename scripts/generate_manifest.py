"""
generate_manifest.py — Create or update an Icechunk repository from a local Zarr store.

The commit is idempotent: if the target branch already has a snapshot the
script exits early, so running it multiple times is safe.

Usage:
    pixi run python scripts/generate_manifest.py --zarr-source data/sample_2026032000_v3.zarr
    pixi run python scripts/generate_manifest.py --zarr-source data/sample_2026032000_v3.zarr --repo stores/my_repo
    pixi run python scripts/generate_manifest.py --zarr-source data/sample_2026032000_v3.zarr --branch main
"""

import argparse
import os

import icechunk
import xarray as xr


def get_or_create_repo(
    repo_path: str,
    zarr_source: str,
) -> icechunk.Repository:
    storage = icechunk.local_filesystem_storage(repo_path)

    config = icechunk.RepositoryConfig.default()
    config.set_virtual_chunk_container(
        icechunk.VirtualChunkContainer(
            f"file://{os.path.abspath(zarr_source)}/",
            icechunk.local_filesystem_store(zarr_source),
        )
    )

    if os.path.exists(repo_path) and os.listdir(repo_path):
        print(f"Opening existing Icechunk repo: {repo_path}")
        return icechunk.Repository.open(storage)

    os.makedirs(repo_path, exist_ok=True)
    print(f"Creating new Icechunk repo: {repo_path}")
    return icechunk.Repository.create(storage, config)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Commit a local Zarr store into an Icechunk repository."
    )
    parser.add_argument(
        "--zarr-source",
        type=str,
        required=True,
        help="Path to the source Zarr store.",
    )
    parser.add_argument(
        "--repo",
        type=str,
        default="stores/icechunk_repo",
        help="Path to the Icechunk repository (default: stores/icechunk_repo).",
    )
    parser.add_argument(
        "--branch",
        type=str,
        default="main",
        help="Branch to commit to (default: main).",
    )
    args = parser.parse_args()

    if not os.path.exists(args.zarr_source):
        raise FileNotFoundError(f"Zarr source not found: {args.zarr_source}")

    repo = get_or_create_repo(args.repo, args.zarr_source)

    try:
        snapshots = list(repo.ancestry(args.branch))
    except Exception:
        snapshots = []

    if snapshots:
        print(f"Branch '{args.branch}' already has a snapshot — skipping commit.")
        print(f"Latest snapshot: {snapshots[0]}")
        return

    ds = xr.open_zarr(args.zarr_source, consolidated=False)

    session = repo.writable_session(args.branch)
    ds.to_zarr(session.store, mode="w")
    snapshot_id = session.commit(f"Import {os.path.basename(args.zarr_source)}")

    print(f"✅ Commit successful — snapshot ID: {snapshot_id}")
    print(ds)


if __name__ == "__main__":
    main()
