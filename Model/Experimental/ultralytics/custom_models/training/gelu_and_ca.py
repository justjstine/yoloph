import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from ultralytics import YOLO

def main():
    model = YOLO("custom_models/yolov8s-ca-gelu-seg.yaml")

    results = model.train(
        data=r"custom_models/training/Combined Dataset/data.yaml",
        epochs=100,
        imgsz=640,
        batch=2,
        device=0,
        workers=2,
        name="yolov8s-ca-gelu-seg"
    )


if __name__ == "__main__":
    main()