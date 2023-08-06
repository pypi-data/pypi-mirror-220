from __future__ import annotations

import sys
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import toml

from slice_to_py_dist.types import DistPackageInfo, SliceToPyDistError
from slice_to_py_dist.utils import parse_author


BACKEND_DIR = "custom_build_backend"  # Must exist next to current __file__
BACKEND_MODULE = "backend.py"


SLICE_SUFFIX = ".ice"


def find_slice_files(directory: Path) -> list[Path]:
    slice_files = [p.relative_to(directory) for p in directory.glob(f"**/*{SLICE_SUFFIX}")]
    if len(slice_files) == 0:
        raise SliceToPyDistError(f"Can't find {SLICE_SUFFIX} files under {directory.absolute()}")
    return slice_files


def expand_path(path: Path) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(path)))


def prepare_build_dir(
    build_dir: Path, slice_source_dir: Path, slice_storage_package: str, dist_info: DistPackageInfo
) -> None:
    # Find input slice files.
    slice_source_dir = expand_path(slice_source_dir)
    slice_files = find_slice_files(slice_source_dir)
    print(f"Found {len(slice_files)} slice files in {str(slice_source_dir)}")

    # Copy the directory of the custom build backend, also check backend module in it.
    backend_dir_src = Path(__file__).parent / BACKEND_DIR
    backend_module = backend_dir_src / BACKEND_MODULE
    if not backend_module.exists():
        raise SliceToPyDistError(f"prepare_build_dir: missing the module: {backend_module}")
    backend_dir_dest = build_dir / BACKEND_DIR
    shutil.copytree(backend_dir_src, backend_dir_dest)

    # Create pyproject.toml
    data = {
        "project": {
            "name": dist_info.name,
            "version": dist_info.version,
            "authors": [parse_author(a) for a in dist_info.authors],
            "description": dist_info.summary,
            "requires-python": dist_info.requires_python,
            "dependencies": ["zeroc-ice"],
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": os.path.splitext(BACKEND_MODULE)[0],
            "backend-path": [BACKEND_DIR],
        },
    }
    with open(build_dir / "pyproject.toml", "xt", encoding="utf-8") as f:
        toml.dump(data, f)

    # Create setup.cfg (for setuptools)
    with open(build_dir / "setup.cfg", "xt", encoding="utf-8") as f:
        f.writelines(
            s + "\n"
            for s in [
                "[options]",
                "packages = find:",
            ]
        )

    # Create the directory for the python import package which will store slice files.
    slice_pkg_dir = build_dir / slice_storage_package
    slice_pkg_dir.mkdir()
    # Create an empty __init__.py file.
    with open(slice_pkg_dir / "__init__.py", "xt", encoding="utf-8"):
        pass
    # Copy slice files.
    for rel_path in slice_files:
        dest_path = slice_pkg_dir / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure that destination directory exists.
        shutil.copyfile(slice_source_dir / rel_path, dest_path)

    # Create manifest file.
    manifest_file = build_dir / "MANIFEST.in"
    with open(manifest_file, "xt", encoding="utf-8") as f:
        f.writelines(
            s + "\n"
            for s in [
                f"graft {BACKEND_DIR}",
                f"graft {slice_storage_package}",
                "global-exclude *.py[cod]",
            ]
        )


def build_sdist(slice_source_dir: str, slice_storage_package: str, dist_info: DistPackageInfo) -> None:
    with tempfile.TemporaryDirectory() as build_dir:
        build_dir = Path(build_dir)

        print("Preparing temporary build directory...")
        prepare_build_dir(build_dir, Path(slice_source_dir), slice_storage_package, dist_info)

        print("Building the sdist package...")
        args = f"{sys.executable} -m build --sdist".split()
        completed = subprocess.run(args, cwd=build_dir, check=False)
        if completed.returncode != 0:
            raise SliceToPyDistError(f"Command {args} failed with code {completed.returncode}")

        print("Copying the newly built sdist to the current directory...")
        dist_dir = build_dir / "dist"
        dist_files = [p.relative_to(dist_dir) for p in dist_dir.glob("*.tar.gz")]
        if len(dist_files) == 0:
            raise SliceToPyDistError(f"Can't find newly built sdist files under {dist_dir.absolute()}")
        for rel_path in dist_files:
            print(rel_path)
            shutil.copyfile(dist_dir / rel_path, Path(".") / rel_path)
