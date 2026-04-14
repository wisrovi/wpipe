#!/usr/bin/env python3
"""
File Date Mapper - Map and organize files by date

Usage:
    python map_files.py --source project/ --start 2025-05-01 --end 2026-01-31
"""

import argparse
import csv
from datetime import datetime
from pathlib import Path
import shutil


def get_file_dates(file_path: Path) -> tuple[datetime, datetime]:
    """Get creation and modification dates for a file."""
    stat = file_path.stat()
    mtime = datetime.fromtimestamp(stat.st_mtime)
    ctime = datetime.fromtimestamp(stat.st_ctime)
    return ctime, mtime


def is_in_range(date: datetime, start: datetime, end: datetime) -> bool:
    """Check if date is within range."""
    return start <= date <= end


def generate_mapping(
    source: Path, start: datetime, end: datetime, dest: Path
) -> list[dict]:
    """Generate file mapping and move files within date range."""
    mapping = []

    for file_path in sorted(source.rglob("*")):
        if not file_path.is_file():
            continue

        ctime, mtime = get_file_dates(file_path)

        in_range = is_in_range(mtime, start, end)

        if in_range and dest:
            rel_path = file_path.relative_to(source)
            dest_path = dest / rel_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, dest_path)

        mapping.append(
            {
                "path_original": str(file_path),
                "fecha_creacion": ctime.isoformat(),
                "fecha_edicion": mtime.isoformat(),
                "en_rango_fechas": "TRUE" if in_range else "FALSE",
                "path_destino": str(dest / file_path.relative_to(source))
                if in_range and dest
                else "",
            }
        )

    return mapping


def write_csv(mapping: list[dict], output: Path) -> None:
    """Write mapping to CSV file."""
    if not mapping:
        return

    with open(output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=mapping[0].keys())
        writer.writeheader()
        writer.writerows(mapping)


def main():
    parser = argparse.ArgumentParser(description="Map files by date")
    parser.add_argument("--source", "-s", required=True, help="Source directory")
    parser.add_argument(
        "--dest", "-d", default="evidencias", help="Destination directory"
    )
    parser.add_argument("--start", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("--output", "-o", default="file_mapping.csv", help="CSV output")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    dest = Path(args.dest).resolve()
    start = datetime.strptime(args.start, "%Y-%m-%d")
    end = datetime.strptime(args.end, "%Y-%m-%d")

    print(f"📂 Analyzing: {source}")
    print(f"📅 Range: {start.date()} to {end.date()}")
    print(f"📁 Output: {dest}")

    mapping = generate_mapping(source, start, end, dest)
    write_csv(mapping, Path(args.output))

    in_range = sum(1 for m in mapping if m["en_rango_fechas"] == "TRUE")

    print(f"\n✅ Complete!")
    print(f"   Total files: {len(mapping)}")
    print(f"   In range: {in_range}")
    print(f"   CSV: {args.output}")


if __name__ == "__main__":
    main()
