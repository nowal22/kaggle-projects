"""Utility helpers for working with Kaggle datasets.

This module wraps the `kaggle` command-line tool to download and unpack
datasets into a local data folder. It is intentionally simple — it shells
out to the `kaggle` CLI rather than depending on the Kaggle Python API
internals, so it stays robust to upstream changes.

Prerequisites:
    - The `kaggle` package is installed (see requirements.txt).
    - A valid API token is placed at ~/.kaggle/kaggle.json (chmod 600).
      See README.md -> "Getting Started -> Set up the Kaggle API".
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def download_dataset(dataset_slug: str, dest_dir: str | os.PathLike) -> Path:
    """Download and unzip a Kaggle dataset into a target folder.

    Shells out to the `kaggle datasets download` CLI, which requires that
    `kaggle.json` credentials are configured (see module docstring).

    Args:
        dataset_slug: The Kaggle dataset slug in the form "owner/dataset-name",
            e.g. "kaggle/titanic" or "bensaid08/titanic-train-test-data".
        dest_dir: Directory to download into. Created (with parents) if it
            does not already exist.

    Returns:
        The absolute path to the destination directory containing the
        unzipped dataset files.

    Raises:
        FileNotFoundError: If the `kaggle` executable is not on PATH.
        subprocess.CalledProcessError: If the `kaggle` CLI exits non-zero.
    """
    dest_path = Path(dest_dir).expanduser().resolve()
    dest_path.mkdir(parents=True, exist_ok=True)

    # Ensure the kaggle CLI is available before doing real work.
    import shutil

    if shutil.which("kaggle") is None:
        raise FileNotFoundError(
            "The `kaggle` CLI was not found on PATH. Install it with "
            "`pip install kaggle` and configure ~/.kaggle/kaggle.json."
        )

    cmd = [
        "kaggle",
        "datasets",
        "download",
        dataset_slug,
        "--unzip",
        "--path",
        str(dest_path),
    ]

    print(f"Downloading {dataset_slug} -> {dest_path}", file=sys.stderr)
    subprocess.run(cmd, check=True)
    return dest_path


if __name__ == "__main__":
    # Example usage (do NOT run automatically during scaffolding):
    #   python utils/kaggle_download.py
    import argparse

    parser = argparse.ArgumentParser(description="Download a Kaggle dataset.")
    parser.add_argument("slug", help='Dataset slug, e.g. "owner/dataset-name"')
    parser.add_argument("dest", help="Destination directory")
    args = parser.parse_args()
    download_dataset(args.slug, args.dest)
