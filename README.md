# Icechunk Sandbox

Icechunk Sandbox is a workspace dedicated to experimenting with Icechunk, an open-source transactional storage engine for Zarr that provides Git-like version control and safe concurrent data access.

## Objective

The primary purpose of this repository is to experiment with Icechunk manifests and the underlying Zarr storage mechanisms.

## Core Dependencies

This project uses [Pixi](https://pixi.sh) to manage the Python environment and its dependencies. The core libraries driving this sandbox include:

- **Icechunk:** The central dependency of this project, enabling experiments with transactional storage, dataset branching, and manifests.
- **Xarray:** Used to create, format, and manipulate the N-dimensional labeled data arrays before they are written to disk.
- **Zarr:** The underlying storage format library handling how the chunked, compressed N-dimensional data is saved and read.
- **Pandas & Numpy:** Utilized alongside Xarray to generate the time series and numerical bounds for the mock datasets.

## Installation

Follow these steps to set up the workspace using Pixi:

**1. Install Pixi (if not already installed)**

```bash
# Works for both macOS and Linux environment
curl -fsSL https://pixi.sh/install.sh | bash
source ~/.$(basename $SHELL)rc
```

## Usage
pixi run python create_zarr.py
# Pour inspecter le format Zarr v2 ou v3
ls -R temperature_data.zarr

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


### The Power of Consolidated Metadata: Zarr v2 vs. Zarr v3

**Why Consolidate Metadata?**
By default, Zarr stores the metadata for each array and group in separate, small JSON files distributed across the dataset's directory tree. While this works well for local file systems, it becomes a major performance bottleneck when working with cloud object storage (like AWS S3, Google Cloud Storage, or Azure Blob). Fetching hundreds or thousands of small metadata files over a network introduces significant latency.

"Consolidating" metadata solves this issue by aggregating all the hierarchy and array metadata into a single file. This allows the Zarr client to understand the entire dataset structure with just one single network request. The benefits are substantial:
* **Drastically reduced initialization time:** Opening a dataset takes a fraction of the time.
* **Fewer API calls:** Reduces costs and avoids throttling on cloud storage providers.
* **Better overall read performance:** The client can immediately start fetching the actual data chunks.

---

**Zarr v2: The `.zmetadata` Add-on**
In Zarr v2, consolidated metadata was introduced as a necessary workaround to solve cloud performance issues.
* **Creation:** It is an opt-in feature. You must explicitly run a consolidation step (e.g., `zarr.consolidate_metadata()`), which crawls the dataset tree and generates a `.zmetadata` file at the root.
* **Usage:** Clients must be explicitly told to look for this file, typically by using a specific function like `zarr.open_consolidated()`. 
* **Maintenance:** If the structure of the dataset changes (e.g., a new array is added), the `.zmetadata` file falls out of sync and must be manually updated.

**Zarr v3: A Modern, Standardized Approach**
Zarr v3 was built from the ground up with cloud-native performance in mind and completely refactors how metadata is structured.
* **Unified Format:** Instead of scattering `.zarray`, `.zattrs`, and `.zgroup` files everywhere, Zarr v3 standardizes metadata into `zarr.json` files.
* **Integrated Consolidation:** Rather than relying on a bolted-on `.zmetadata` workaround, Zarr v3 handles consolidated metadata through its formalized extension mechanism. It is designed to be natively integrated into the specification.
* **Transparent Usage:** Because metadata handling is standardized, clients can interact with Zarr v3 stores more intelligently and transparently, without needing separate, ad-hoc API calls just to read an aggregated metadata file.
