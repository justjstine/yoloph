import torch
import ultralytics

from ultralytics import YOLO
from ultralytics.nn.modules import ConvGELU, CoordinateAttention


print("=" * 60)
print("ULTRALYTICS LOCATION")
print("=" * 60)

print(ultralytics.__file__)


print("\n" + "=" * 60)
print("CUSTOM MODULE TEST")
print("=" * 60)

print("ConvGELU:")
print(ConvGELU)

print("\nCoordinateAttention:")
print(CoordinateAttention)


print("\n" + "=" * 60)
print("BUILDING MODEL")
print("=" * 60)

model = YOLO(
    "custom_models/yolov8s-ca-gelu-p2ref-seg.yaml"
)


print("\n" + "=" * 60)
print("MODEL SUMMARY")
print("=" * 60)

model.info(verbose=True)


print("\n" + "=" * 60)
print("MODEL LAYERS")
print("=" * 60)

print(model.model.model)


print("\n" + "=" * 60)
print("DUMMY FORWARD PASS")
print("=" * 60)

x = torch.randn(
    1,
    3,
    640,
    640
)

model.model.eval()

with torch.no_grad():

    output = model.model(x)


print("Forward pass successful.")
print("Input shape:", x.shape)