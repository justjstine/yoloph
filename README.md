# YOLO-PH: An Enhanced YOLOv8 Architecture for Pothole Classification Using Reference Scale Image Calibration

YOLO-PH is an undergraduate thesis project focused on improving pothole detection and classification using an enhanced YOLOv8 pipeline with reference-scale image calibration.

## Overview

This repository contains:
- Multi-source pothole datasets and annotations
- Data-cleaning and conversion scripts
- Baseline training artifacts and results
- Experimental model workspace based on Ultralytics YOLOv8

## Thesis Information

- **Title:** YOLO-PH: An Enhanced YOLOv8 Architecture for Pothole Classification Using Reference Scale Image Calibration
- **Domain:** Computer Vision, Road Surface Defect Analysis
- **Primary Framework:** YOLOv8 (Ultralytics)

## Repository Structure

```text
Dataset/
  Combined Dataset/
  Kaggle 2/dataset/
  RoboFlow/
  Roboflow 2/

Model/
  Baseline Model/
    Baseline Results/
    Cleaning/
  Experimental Model/
    ultralytics/
```

## Key Files

- Dataset configs:
  - `Dataset/RoboFlow/data.yaml`
  - `Dataset/Kaggle 2/dataset/data.yaml`
- Data processing scripts:
  - `Model/Baseline Model/Cleaning/convert_coco_to_yolov8_seg.py`
  - `Model/Baseline Model/Cleaning/Duplicate.py`
  - `Model/Baseline Model/Cleaning/Nonpothole_images.py`
- Baseline training artifacts:
  - `Model/Baseline Model/Baseline Results/args.yaml`
  - `Model/Baseline Model/Baseline Results/results.csv`

## Requirements

- Python 3.12.13
- Conda (Miniconda or Anaconda)
- pip (latest recommended)

Install all project dependencies from:

- `requirements.txt`

## Setup

1. Create and activate a Conda environment:

```bash
conda create -n yoloph python=3.12.13 -y
conda activate yoloph
```

2. Upgrade pip (recommended):

```bash
python -m pip install --upgrade pip
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Verify your dataset paths inside YAML/config files before training.

## Baseline Training Example

```bash
yolo task=segment mode=train model=yolov8s-seg.pt data=Dataset/RoboFlow/data.yaml epochs=100 imgsz=640
```

## Reproducibility Notes

- Keep dataset splits (`train`, `valid/val`, `test`) consistent across experiments.
- Track all hyperparameters in YAML or experiment logs.
- Store model weights and large artifacts outside regular Git history or in Git LFS.



