import os

labels_folder = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\Thesis Potholes 2.yolov8\valid\labels"

bbox_removed = 0
other_classes_removed = 0
kept = 0
background = 0

for filename in os.listdir(labels_folder):
    if not filename.endswith(".txt"):
        continue

    path = os.path.join(labels_folder, filename)

    with open(path, "r") as f:
        lines = f.readlines()

    new_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        values = line.split()

        # Skip bounding boxes
        if len(values) == 5:
            bbox_removed += 1
            continue

        # Keep only class 0 segmentation
        if values[0] == "0":
            new_lines.append(line + "\n")
            kept += 1
        else:
            other_classes_removed += 1

    with open(path, "w") as f:
        f.writelines(new_lines)

    if len(new_lines) == 0:
        background += 1

print("=" * 40)
print(f"Bounding boxes removed : {bbox_removed}")
print(f"Other classes removed  : {other_classes_removed}")
print(f"Pothole polygons kept  : {kept}")
print(f"Background images      : {background}")
print("=" * 40)