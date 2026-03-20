"""
create_sample_zarr.py — Generate a synthetic Zarr dataset for experimentation.

Usage:
    pixi run python scripts/create_sample_zarr.py
    pixi run python scripts/create_sample_zarr.py --version 2
    pixi run python scripts/create_sample_zarr.py --version 3 --consolidated
    pixi run python scripts/create_sample_zarr.py --output-dir data/
"""

import argparse
import os

import numpy as np
import pandas as pd
import xarray as xr


def build_dataset(run_time: pd.Timestamp) -> xr.Dataset:
    times = pd.date_range(run_time, periods=48, freq="1h")
    lats = np.arange(-90, 91, 1.0)
    lons = np.arange(0, 360, 1.0)

    ds = xr.Dataset(
        data_vars={
            "air_temperature": (
                ["time", "lat", "lon"],
                np.random.uniform(-20, 40, (len(times), len(lats), len(lons))),
                {"units": "Celsius", "long_name": "Air Temperature"},
            )
        },
        coords={
            "time": times,
            "lat": (["lat"], lats, {"units": "degrees_north"}),
            "lon": (["lon"], lons, {"units": "degrees_east"}),
        },
        attrs={
            "description": "Synthetic temperature dataset for Icechunk/Zarr experimentation."
        },
    )
    return ds.chunk({"time": 5, "lat": 90, "lon": 90})


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Write a synthetic Zarr dataset to disk."
    )
    parser.add_argument("--version", type=int, choices=[2, 3], default=3)
    parser.add_argument("--consolidated", action="store_true", default=False)
    parser.add_argument("--output-dir", type=str, default="./data")
    args = parser.parse_args()

    run_time = pd.Timestamp.now(tz="UTC").floor("D").tz_localize(None)
    consolidated_suffix = "_c" if args.consolidated else ""
    zarr_path = os.path.join(
        args.output_dir,
        f"sample_{run_time:%Y%m%d%H}_v{args.version}{consolidated_suffix}.zarr",
    )

    ds = build_dataset(run_time)
    ds.to_zarr(
        zarr_path, mode="w", zarr_format=args.version, consolidated=args.consolidated
    )

    label = "consolidated" if args.consolidated else "no consolidation"
    print(f"✅ Zarr v{args.version} ({label}) written to: {zarr_path}")
    print(ds)


if __name__ == "__main__":
    main()
