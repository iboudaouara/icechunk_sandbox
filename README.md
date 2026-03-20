# Icechunk Sandbox

Experiments with Icechunk — a transactional storage engine for Zarr with Git-like versioning.

## Objective

- Understand Icechunk manifests and snapshot mechanics
- Understand Zarr v2/v3 on-disk differences and when consolidated metadata matters
- Prototype a conversion pipeline from RPN FST to Zarr

## Setup
 
```bash
curl -fsSL https://pixi.sh/install.sh | bash
source ~/.$(basename $SHELL)rc
pixi install
```

## Usage
 
### Write a synthetic Zarr dataset

```bash
pixi run python scripts/create_sample_zarr.py [--version 2|3] [--consolidated] [--output-dir data/]
```
 
### Commit a Zarr store into an Icechunk repo

```bash
pixi run python scripts/generate_manifest.py --zarr-source data/sample_*.zarr [--repo stores/repo] [--branch main]
```

## Dataset naming
 
`sample_{YYYYMMDDHH}_v{2|3}[_c].zarr` — synthetic temperature data, not real observations. `_c` suffix indicates consolidated metadata.

## Zarr v2 vs v3
 
| | v2 | v3 |
|---|---|---|
| Metadata | `.zarray` / `.zgroup` files | `zarr.json` |
| Consolidation | Manual (`.zmetadata`) | Built-in |
| Chunks | `var/0.0.0` | `var/c/0/0/0` |
| Sharding | Not supported | Multiple chunks per file |

Consolidation aggregates all metadata into a single file, reducing cloud API calls.

## Dependencies
 
| Package | Role |
|---|---|
| `icechunk` | Versioned store — branching, snapshots, manifests |
| `zarr` | Chunked N-dimensional array format |
| `xarray` | Labeled array manipulation and Zarr I/O |
| `dask` | Lazy parallel computation for chunked arrays |
| `numpy` / `pandas` | Synthetic data generation |

## References
 
- [Icechunk](https://icechunk.io)
- [Zarr](https://zarr.dev)
- [Pixi](https://pixi.sh)
