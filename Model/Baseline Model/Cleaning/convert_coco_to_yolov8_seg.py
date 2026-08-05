from __future__ import annotations

import argparse
import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Iterable


DEFAULT_SOURCE_DIR = Path(
    r"C:\Users\almad\Desktop\Thesis\Model\Baseline Model\Roboflow 2"
)
DEFAULT_OUTPUT_DIR = DEFAULT_SOURCE_DIR.parent / f"{DEFAULT_SOURCE_DIR.name}_YOLOv8_Seg"
SPLITS = ("train", "valid", "test")


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def normalized_polygon(points: Iterable[float], width: int, height: int) -> list[float]:
    values = list(points)
    if len(values) < 6 or len(values) % 2 != 0:
        return []

    normalized: list[float] = []
    for index in range(0, len(values), 2):
        x = clamp(float(values[index]) / width)
        y = clamp(float(values[index + 1]) / height)
        normalized.extend([x, y])
    return normalized


def format_label_line(class_index: int, polygon: list[float]) -> str:
    coords = " ".join(f"{value:.6f}" for value in polygon)
    return f"{class_index} {coords}"


def convert_split(source_dir: Path, output_dir: Path, split: str) -> tuple[int, int, dict[int, str]]:
    annotation_path = source_dir / split / "_annotations.coco.json"
    if not annotation_path.exists():
        raise FileNotFoundError(f"Missing annotation file: {annotation_path}")

    with annotation_path.open("r", encoding="utf-8") as handle:
        coco = json.load(handle)

    categories = {
        category["id"]: category["name"]
        for category in coco.get("categories", [])
    }
    annotations = coco.get("annotations", [])
    images = coco.get("images", [])

    used_category_ids = sorted({annotation["category_id"] for annotation in annotations})
    class_mapping = {category_id: index for index, category_id in enumerate(used_category_ids)}

    image_lookup = {image["id"]: image for image in images}
    annotations_by_image: dict[int, list[dict]] = defaultdict(list)
    for annotation in annotations:
        annotations_by_image[annotation["image_id"]].append(annotation)

    split_image_source = source_dir / split
    split_image_output = output_dir / split / "images"
    split_label_output = output_dir / split / "labels"
    split_image_output.mkdir(parents=True, exist_ok=True)
    split_label_output.mkdir(parents=True, exist_ok=True)

    image_count = 0
    label_count = 0

    for image_id, image in image_lookup.items():
        file_name = image["file_name"]
        source_image_path = split_image_source / file_name
        target_image_path = split_image_output / file_name
        target_label_path = split_label_output / f"{Path(file_name).stem}.txt"

        if not source_image_path.exists():
            raise FileNotFoundError(f"Missing image file: {source_image_path}")

        shutil.copy2(source_image_path, target_image_path)
        image_count += 1

        width = int(image["width"])
        height = int(image["height"])
        lines: list[str] = []

        for annotation in annotations_by_image.get(image_id, []):
            category_id = annotation["category_id"]
            class_index = class_mapping.get(category_id)
            if class_index is None:
                continue

            segmentation = annotation.get("segmentation", [])
            if not isinstance(segmentation, list):
                continue

            for polygon in segmentation:
                if not isinstance(polygon, list):
                    continue

                normalized = normalized_polygon(polygon, width, height)
                if not normalized:
                    continue

                lines.append(format_label_line(class_index, normalized))

        target_label_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        label_count += 1

    class_names = {class_mapping[category_id]: categories.get(category_id, f"class_{category_id}") for category_id in used_category_ids}
    return image_count, label_count, class_names


def write_data_yaml(output_dir: Path, class_names: dict[int, str]) -> None:
    ordered_names = [class_names[index] for index in sorted(class_names)]
    yaml_path = output_dir / "data.yaml"
    yaml_lines = [
        f"path: {output_dir.as_posix()}",
        "train: train/images",
        "val: valid/images",
        "test: test/images",
        f"nc: {len(ordered_names)}",
        f"names: {ordered_names!r}",
    ]
    yaml_path.write_text("\n".join(yaml_lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a Roboflow COCO instance-segmentation export to YOLOv8 segmentation format."
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE_DIR, help="Path to the COCO export folder")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR, help="Destination YOLOv8 dataset folder")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dir: Path = args.source
    output_dir: Path = args.output

    if not source_dir.exists():
        raise FileNotFoundError(f"Source folder not found: {source_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    total_images = 0
    total_labels = 0
    class_names: dict[int, str] = {}

    for split in SPLITS:
        image_count, label_count, split_class_names = convert_split(source_dir, output_dir, split)
        total_images += image_count
        total_labels += label_count
        if not class_names:
            class_names = split_class_names

    write_data_yaml(output_dir, class_names)

    print(f"Converted dataset written to: {output_dir}")
    print(f"Images copied: {total_images}")
    print(f"Label files written: {total_labels}")
    print(f"Classes: {[class_names[index] for index in sorted(class_names)]}")


if __name__ == "__main__":
    main()