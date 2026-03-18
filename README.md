# Icechunk Sandbox

Icechunk Sandbox is a workspace dedicated to experimenting with Icechunk, an open-source transactional storage engine for Zarr that provides Git-like version control and safe concurrent data access.

## Installation

This project uses [Pixi](https://pixi.sh) to manage the Python environment and dependencies.

Follow these steps to set up the workspace:

**1. Install Pixi (if not already installed)**

```bash
curl -fsSL https://pixi.sh/install.sh | bash


source ~/.$(basename $SHELL)rc
```

## Data Naming Convention
All raw datasets follow the pattern: `gdps_{TIMESTAMP}_{VERSION}.zarr`
- **TIMESTAMP**: YYYYMMDDHH (Model run start time)
- **VERSION**: v2 (Legacy) or v3 (Next-gen)

### Zarr v2 (Legacy)
- Uses `.zarray` and `.zgroup` files for metadata.
- Chunks are stored as flat files at the root of the variable folder (e.g., `air_temperature/0.0.0`).


### Zarr v3 (Modern)
- Uses a unified `zarr.json` for metadata.
- Chunks are stored in a specific namespace directory (e.g., `air_temperature/c/0/0/0`).
- Supports **sharding**, allowing multiple chunks to be stored in a single file for better cloud performance.
