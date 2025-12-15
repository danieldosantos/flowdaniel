from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).parent
OUTPUT_FILE = ROOT / "bestiary-ultimate.json"


def find_bestiary_files(root: Path) -> list[Path]:
    return sorted(
        p
        for p in root.rglob("*.json")
        if "bestiary" in p.stem.lower() and p.name != OUTPUT_FILE.name
    )


def load_json(file_path: Path) -> Any:
    with file_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def merge_payloads(files: Iterable[Path]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    for file_path in files:
        payload = load_json(file_path)
        if isinstance(payload, list):
            merged.extend({"source": str(file_path.relative_to(ROOT)), "entry": item} for item in payload)
        else:
            merged.append({"source": str(file_path.relative_to(ROOT)), "entry": payload})
    return merged


def save_output(entries: list[dict[str, Any]]) -> None:
    with OUTPUT_FILE.open("w", encoding="utf-8") as handle:
        json.dump(entries, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def main() -> None:
    files = find_bestiary_files(ROOT)
    merged_entries = merge_payloads(files)
    save_output(merged_entries)
    print(f"Merged {len(files)} bestiary file(s) into {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
