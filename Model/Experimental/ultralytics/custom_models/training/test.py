from pathlib import Path

import torch
import torch.nn as nn
import ultralytics

from ultralytics import YOLO
from ultralytics.nn.modules import Conv


# ============================================================
# MODEL PATH
# ============================================================

MODEL_YAML = Path(
    "custom_models/yolov8s-ca-gelu-p2ref-seg.yaml"
).resolve()


print("=" * 70)
print("ULTRALYTICS")
print("=" * 70)

print("Loaded from:")
print(ultralytics.__file__)

print("\nModel YAML:")
print(MODEL_YAML)

print("\nExists:")
print(MODEL_YAML.exists())


# ============================================================
# BUILD MODEL
# ============================================================

print("\n" + "=" * 70)
print("BUILDING MODEL")
print("=" * 70)


model = YOLO(
    str(MODEL_YAML),
    task="segment"
)


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("MODEL SUMMARY")
print("=" * 70)


model.info(
    verbose=True
)


# ============================================================
# COUNT ACTIVATION MODULES
# ============================================================

gelu_count = 0
silu_count = 0
hardswish_count = 0
relu_count = 0
identity_count = 0


gelu_locations = []
silu_locations = []
hardswish_locations = []


for name, module in model.model.named_modules():

    if isinstance(module, nn.GELU):

        gelu_count += 1
        gelu_locations.append(name)

    elif isinstance(module, nn.SiLU):

        silu_count += 1
        silu_locations.append(name)

    elif isinstance(module, nn.Hardswish):

        hardswish_count += 1
        hardswish_locations.append(name)

    elif isinstance(module, nn.ReLU):

        relu_count += 1

    elif isinstance(module, nn.Identity):

        identity_count += 1


print("\n" + "=" * 70)
print("ACTIVATION COUNTS")
print("=" * 70)

print("GELU:      ", gelu_count)
print("SiLU:      ", silu_count)
print("Hardswish: ", hardswish_count)
print("ReLU:      ", relu_count)
print("Identity:  ", identity_count)


# ============================================================
# CHECK EVERY STANDARD ULTRALYTICS CONV
# ============================================================

print("\n" + "=" * 70)
print("STANDARD CONV ACTIVATION CHECK")
print("=" * 70)


total_conv = 0

conv_gelu = 0
conv_silu = 0
conv_identity = 0
conv_other = 0


bad_conv_locations = []


for name, module in model.model.named_modules():

    if isinstance(module, Conv):

        total_conv += 1

        if isinstance(module.act, nn.GELU):

            conv_gelu += 1

        elif isinstance(module.act, nn.SiLU):

            conv_silu += 1
            bad_conv_locations.append(name)

        elif isinstance(module.act, nn.Identity):

            conv_identity += 1

        else:

            conv_other += 1

            print(
                "Other activation:",
                name,
                type(module.act).__name__
            )


print("Total Conv blocks:      ", total_conv)

print(
    "Conv using GELU:        ",
    conv_gelu
)

print(
    "Conv using SiLU:        ",
    conv_silu
)

print(
    "Conv using Identity:    ",
    conv_identity
)

print(
    "Conv using other act:   ",
    conv_other
)

# ============================================================
# PRINT EVERY CONV ACTIVATION
# ============================================================

print("\n" + "=" * 70)
print("ALL CONV ACTIVATIONS")
print("=" * 70)

for name, module in model.model.named_modules():

    if isinstance(module, Conv):

        print(
            f"{name:<45}",
            type(module.act).__name__
        )


# ============================================================
# SHOW ANY REMAINING SILU
# ============================================================

print("\n" + "=" * 70)
print("REMAINING SILU LOCATIONS")
print("=" * 70)


if silu_locations:

    for location in silu_locations:

        print(location)

else:

    print(
        "No nn.SiLU modules found."
    )


# ============================================================
# SHOW HARDSWISH
# ============================================================

print("\n" + "=" * 70)
print("HARDSWISH LOCATIONS")
print("=" * 70)


for location in hardswish_locations:

    print(location)


# ============================================================
# TEST RESULT
# ============================================================

print("\n" + "=" * 70)
print("GLOBAL GELU RESULT")
print("=" * 70)


if conv_silu == 0:

    print(
        "PASS:"
    )

    print(
        "No standard Ultralytics Conv block uses SiLU."
    )

else:

    print(
        "FAIL:"
    )

    print(
        conv_silu,
        "standard Conv blocks still use SiLU."
    )

    print(
        "Locations:"
    )

    for location in bad_conv_locations:

        print(location)


# ============================================================
# DUMMY FORWARD PASS
# ============================================================

print("\n" + "=" * 70)
print("DUMMY FORWARD PASS")
print("=" * 70)


x = torch.randn(
    1,
    3,
    640,
    640
)


model.model.eval()


with torch.no_grad():

    output = model.model(x)


print(
    "Forward pass successful."
)

print(
    "Input shape:",
    x.shape
)

