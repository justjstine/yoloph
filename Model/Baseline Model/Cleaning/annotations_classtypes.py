import os
from collections import Counter

labels_dir = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\FINAL Dataset\train\labels"

image_counts = Counter()

for filename in os.listdir(labels_dir):
    if not filename.endswith(".txt"):
        continue

    label_path = os.path.join(labels_dir, filename)

    classes_in_image = set()

    with open(label_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                classes_in_image.add(line.split()[0])

    for cls in classes_in_image:
        image_counts[cls] += 1

print("Images containing each class:\n")

for cls, count in sorted(image_counts.items(), key=lambda x: int(x[0])):
    print(f"Class {cls}: {count} images")