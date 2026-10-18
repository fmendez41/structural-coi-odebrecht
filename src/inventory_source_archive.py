"""Create a checksum inventory for a local source archive without redistributing it."""

from __future__ import annotations

import argparse
import csv
import hashlib
import zipfile
from pathlib import Path, PurePosixPath


DOCUMENT_EXTENSIONS = {".pdf", ".html", ".htm"}
NOTEBOOK_EXTENSIONS = {".ipynb"}
GRAPH_EXTENSIONS = {".gexf", ".graphml", ".gephi"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
WEB_ASSET_EXTENSIONS = {".css", ".js", ".gif", ".svg"}


def classify(path: PurePosixPath) -> str:
    extension = path.suffix.lower()
    if extension in DOCUMENT_EXTENSIONS:
        return "documentary_source"
    if extension in NOTEBOOK_EXTENSIONS:
        return "construction_notebook"
    if extension in GRAPH_EXTENSIONS:
        return "graph_data"
    if extension in IMAGE_EXTENSIONS:
        return "image_or_scan"
    if extension in WEB_ASSET_EXTENSIONS:
        return "saved_web_asset"
    return "other"


def redistribution_status(category: str) -> str:
    if category == "construction_notebook":
        return "included_as_original_research_material"
    if category == "graph_data":
        return "inventory_only_existing_repository_graphs_preferred"
    return "inventory_only_not_redistributed_rights_unverified"


def digest_entry(archive: zipfile.ZipFile, info: zipfile.ZipInfo) -> str:
    digest = hashlib.sha256()
    with archive.open(info, "r") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    rows: list[dict[str, str | int]] = []
    with zipfile.ZipFile(args.archive) as archive:
        for info in sorted(archive.infolist(), key=lambda item: item.filename.casefold()):
            if info.is_dir():
                continue
            path = PurePosixPath(info.filename)
            category = classify(path)
            rows.append(
                {
                    "archive_path": info.filename,
                    "extension": path.suffix.lower(),
                    "bytes": info.file_size,
                    "sha256": digest_entry(archive, info),
                    "category": category,
                    "redistribution_status": redistribution_status(category),
                }
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
