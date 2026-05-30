#!/usr/bin/env python3
"""Crop named local assets from an image2/imagegen reference slide."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True, help="Reference slide image path.")
    parser.add_argument("--out-dir", required=True, help="Directory for cropped assets.")
    parser.add_argument("--spec", required=True, help="JSON spec with an assets array.")
    parser.add_argument(
        "--contact-sheet",
        action="store_true",
        help="Write crop-contact-sheet.jpg for visual inspection.",
    )
    return parser.parse_args()


def load_spec(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    assets = data.get("assets")
    if not isinstance(assets, list) or not assets:
        raise ValueError("Spec must contain a non-empty 'assets' array.")
    return assets


def resolve_box(item: dict, width: int, height: int) -> tuple[int, int, int, int]:
    if "box" in item:
        box = item["box"]
        if len(box) != 4:
            raise ValueError(f"{item.get('name', '<unnamed>')}: box must have 4 values.")
        return tuple(int(round(float(v))) for v in box)

    if "relBox" in item:
        rel_box = item["relBox"]
        if len(rel_box) != 4:
            raise ValueError(f"{item.get('name', '<unnamed>')}: relBox must have 4 values.")
        x1, y1, x2, y2 = [float(v) for v in rel_box]
        return (
            int(round(x1 * width)),
            int(round(y1 * height)),
            int(round(x2 * width)),
            int(round(y2 * height)),
        )

    raise ValueError(f"{item.get('name', '<unnamed>')}: expected box or relBox.")


def validate_box(name: str, box: tuple[int, int, int, int], width: int, height: int) -> None:
    x1, y1, x2, y2 = box
    if x1 < 0 or y1 < 0 or x2 > width or y2 > height or x2 <= x1 or y2 <= y1:
        raise ValueError(f"{name}: invalid crop box {box} for image size {width}x{height}.")


def write_contact_sheet(paths: list[Path], out_path: Path) -> None:
    thumbs: list[Image.Image] = []
    for path in paths:
        img = Image.open(path).convert("RGBA")
        img.thumbnail((220, 90))
        tile = Image.new("RGBA", (240, 120), "white")
        tile.alpha_composite(img, ((240 - img.width) // 2, 8))
        ImageDraw.Draw(tile).text((8, 100), path.name, fill=(0, 0, 0, 255))
        thumbs.append(tile.convert("RGB"))

    cols = 2
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 240, rows * 120), "white")
    for index, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((index % cols) * 240, (index // cols) * 120))
    sheet.save(out_path, quality=92)


def main() -> None:
    args = parse_args()
    image_path = Path(args.image)
    out_dir = Path(args.out_dir)
    spec_path = Path(args.spec)
    out_dir.mkdir(parents=True, exist_ok=True)

    source = Image.open(image_path).convert("RGBA")
    width, height = source.size
    output_paths: list[Path] = []

    for item in load_spec(spec_path):
        name = item.get("name")
        if not isinstance(name, str) or not name.lower().endswith(".png"):
            raise ValueError("Each asset needs a PNG file name.")
        box = resolve_box(item, width, height)
        validate_box(name, box, width, height)
        crop = source.crop(box)
        out_path = out_dir / name
        crop.save(out_path)
        output_paths.append(out_path)
        print(f"{name}: {box} -> {out_path}")

    if args.contact_sheet:
        sheet_path = out_dir / "crop-contact-sheet.jpg"
        write_contact_sheet(output_paths, sheet_path)
        print(f"contact_sheet: {sheet_path}")


if __name__ == "__main__":
    main()
