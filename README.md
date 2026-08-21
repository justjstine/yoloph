# YOLO-PH: An Enhanced YOLOv8 Architecture for Pothole Classification Using Reference Scale Image Calibration

YOLO-PH is an undergraduate Computer Science thesis project focused on pothole instance segmentation and physical pothole assessment using an enhanced YOLOv8 architecture together with reference-scale image calibration.

The project investigates architectural modifications to YOLOv8s-Seg for improving the detection and segmentation of potholes, particularly small, distant, irregular, and low-contrast potholes captured using smartphone images.

## Overview

This repository contains:

- Multi-source pothole datasets and instance-segmentation annotations
- Dataset cleaning, conversion, and preprocessing scripts
- Baseline YOLOv8s-Seg experiments
- Enhanced YOLOv8s-Seg architectures
- Coordinate Attention implementation
- GELU-based YOLOv8 convolutional blocks
- Direct-P2 segmentation experiments
- Training and validation results
- Experimental workspace based on Ultralytics YOLOv8

## Thesis Information

- **Title:** YOLO-PH: An Enhanced YOLOv8 Architecture for Pothole Classification Using Reference Scale Image Calibration
- **Domain:** Computer Vision, Machine Learning, Road Surface Defect Analysis
- **Primary Task:** Pothole Instance Segmentation
- **Base Architecture:** YOLOv8s-Seg
- **Framework:** Ultralytics YOLOv8
- **Target Input:** Smartphone road images

## Proposed Pipeline

```text
Smartphone Image
       |
       v
Image Preprocessing
       |
       v
Enhanced YOLOv8s-Seg
       |
       +-----------------------------+
       |                             |
       v                             v
Pothole Detection              Instance Mask
       |                             |
       +-------------+---------------+
                     |
                     v
          Reference-Scale Detection
                     |
                     v
           Pixel-to-Real-World
                Calibration
                     |
                     v
          Pothole Size Assessment
                     |
                     v
                  Result
```

The segmentation mask is used to determine the visible region of an individual pothole. A known-size reference marker can then be used to estimate the conversion between image pixels and real-world dimensions.

## Enhanced YOLOv8s-Seg Architecture

The experimental architecture investigates three primary modifications to the standard YOLOv8s-Seg model.

### 1. GELU Activation

The default SiLU activation used by standard YOLOv8 convolutional blocks is replaced with the Gaussian Error Linear Unit (GELU).

```text
Standard YOLOv8:
Conv -> BatchNorm -> SiLU

Enhanced:
Conv -> BatchNorm -> GELU
```

GELU provides a smooth nonlinear transformation of extracted features.

Module-specific activation functions are retained where required. For example, Coordinate Attention continues to use Hardswish according to its original module design.

### 2. Coordinate Attention

Coordinate Attention (CA) modules are incorporated into selected backbone feature levels.

CA is designed to emphasize important visual features while retaining spatial information along the horizontal and vertical dimensions.

The modules are applied around the:

```text
P3 feature level
P4 feature level
P5 feature level
```

This modification is intended to improve the representation of irregular pothole regions while reducing the influence of irrelevant background features.

### 3. Direct P2 Segmentation

Standard YOLOv8s-Seg performs predictions using three primary feature levels:

```text
P3
P4
P5
```

For a 640 x 640 input image:

```text
P3 = 80 x 80
P4 = 40 x 40
P5 = 20 x 20
```

The experimental Direct-P2 architecture additionally incorporates the higher-resolution P2 feature map:

```text
P2 = 160 x 160
```

The segmentation head therefore receives information from four feature levels:

```text
P2
P3
P4
P5
```

The higher-resolution P2 feature level is investigated for preserving fine spatial information that may otherwise be lost during downsampling, particularly for small or distant potholes.

## Segmentation Head

The current experimental Direct-P2 implementation uses the feature inputs:

```text
P3, P2, P4, P5
```

P3 remains the first feature supplied to the standard Ultralytics Segment module so that the mask prototype generator maintains the expected prototype resolution.

P2 remains directly involved in detection and mask-coefficient prediction.

Conceptually:

```text
P3 ------\
P2 -------\
P4 --------> Segment Head
P5 -------/
          |
          +--> Bounding Boxes
          +--> Class Predictions
          +--> Mask Coefficients
          +--> Mask Prototypes
          |
          v
    Instance Masks
```

## Repository Structure

```text
Dataset/
├── Combined Dataset/
├── Kaggle 2/
│   └── dataset/
├── RoboFlow/
└── Roboflow 2/

Model/
├── Baseline Model/
│   ├── Baseline Results/
│   └── Cleaning/
│
└── Experimental Model/
    └── ultralytics/
```

The experimental Ultralytics repository contains the custom modules and model YAML configurations used for the enhanced architectures.

## Key Files

Dataset paths may need to be changed depending on whether training is performed locally or on Kaggle.

### Dataset Processing

```text
Model/Baseline Model/Cleaning/convert_coco_to_yolov8_seg.py
Model/Baseline Model/Cleaning/Duplicate.py
Model/Baseline Model/Cleaning/Nonpothole_images.py
```

### Baseline Results

```text
Model/Baseline Model/Baseline Results 2.0/args.yaml
Model/Baseline Model/Baseline Results 2.0/results.csv
```

### Experimental Architecture

The experimental Ultralytics source contains custom implementations and model configurations for:

```text
Coordinate Attention
GELU activation
CA + GELU
CA + GELU + P2 refinement
CA + GELU + Direct P2
```

## Evaluation Metrics

Because the primary computer-vision task is instance segmentation, the main evaluation metric is:

```text
Mask mAP50-95
```

```text
Mask Precision
Mask Recall
Mask mAP50

Box Precision
Box Recall
Box mAP50
Box mAP50-95
```

Training and validation losses are also monitored for signs of underfitting and overfitting.

## Current Experimental Results

### YOLOv8s-Seg Baseline

```text
Mask mAP50-95: 46.94%
```

## Requirements

- Python 3.12.13
- Conda (Miniconda or Anaconda)
- PyTorch
- Ultralytics
- pip

Install dependencies using:

```bash
pip install -r requirements.txt
```

## Setup

### 1. Create the environment

```bash
conda create -n yoloph python=3.12.13 -y
conda activate yoloph
```

### 2. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify dataset paths

Dataset YAML files may contain machine-specific paths.

Verify:

```yaml
train:
val:
test:
```

## Project Status

The project is currently under active experimental development.

Current research stages include:

```text
[Completed] Dataset preparation
[Completed] YOLOv8s-Seg baseline
[Completed] Coordinate Attention implementation
[Completed] GELU implementation
[Completed] CA + GELU experiment
[Completed] P2 refinement experiment
[Completed] Direct-P2 architecture implementation
[Completed] Direct-P2 training experiment
[In Progress] Controlled architecture comparison
[In Progress] Reference-scale calibration
[In Progress] Physical pothole size assessment
[In Progress] Smartphone-oriented inference evaluation
```

## Disclaimer

This repository is part of an undergraduate research project. Experimental architectures and results may change as controlled ablation studies and additional validation are completed.
