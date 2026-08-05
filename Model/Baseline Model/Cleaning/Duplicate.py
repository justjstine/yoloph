import os
import imagehash
from PIL import Image
from tqdm import tqdm

# ==========================================================
# CONFIGURATION
# ==========================================================

# Dataset A (KEEP)
DATASET_A_IMAGES = "C:\\Users\\almad\\Desktop\\Thesis\\Dataset\\Segementation\\Kaggle 2\\dataset\\train\\images"
DATASET_A_LABELS = "C:\\Users\\almad\\Desktop\\Thesis\\Dataset\\Segementation\\Kaggle 2\\dataset\\train\\labels"

# Dataset B (REMOVE DUPLICATES FROM HERE)
DATASET_B_IMAGES = "C:\\Users\\almad\\Desktop\\Thesis\\Dataset\\Segementation\\Kaggle\\Pothole_Segmentation_YOLOv8\\train\\images"
DATASET_B_LABELS = "C:\\Users\\almad\\Desktop\\Thesis\\Dataset\\Segementation\\Kaggle\\Pothole_Segmentation_YOLOv8\\train\\labels"

# Duplicate threshold
# 0 = exact duplicate only
# 5 = recommended
# 8 = more aggressive
HASH_THRESHOLD = 5

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")

# ==========================================================
# COMPUTE HASHES FOR DATASET A
# ==========================================================

print("Scanning Dataset A...")

datasetA_hashes = []

for file in tqdm(os.listdir(DATASET_A_IMAGES)):
    if file.lower().endswith(IMAGE_EXTENSIONS):

        path = os.path.join(DATASET_A_IMAGES, file)

        try:
            img = Image.open(path).convert("RGB")
            phash = imagehash.phash(img)

            datasetA_hashes.append((phash, file))

        except Exception as e:
            print(f"Error reading {file}: {e}")

print(f"\nDataset A Images: {len(datasetA_hashes)}")

# ==========================================================
# SCAN DATASET B
# ==========================================================

duplicates = []

print("\nScanning Dataset B...")

for file in tqdm(os.listdir(DATASET_B_IMAGES)):

    if not file.lower().endswith(IMAGE_EXTENSIONS):
        continue

    path = os.path.join(DATASET_B_IMAGES, file)

    try:

        img = Image.open(path).convert("RGB")
        hash_b = imagehash.phash(img)

        duplicate_found = False

        for hash_a, file_a in datasetA_hashes:

            distance = hash_b - hash_a

            if distance <= HASH_THRESHOLD:

                duplicates.append((file, file_a, distance))
                duplicate_found = True
                break

        if duplicate_found:
            continue

    except Exception as e:
        print(f"Error reading {file}: {e}")

print("\n======================================")
print("Duplicate Detection Finished")
print("======================================")
print(f"Duplicates Found: {len(duplicates)}")

# ==========================================================
# DELETE DUPLICATES FROM DATASET B
# ==========================================================

deleted = 0

for dup_file, original_file, dist in duplicates:

    image_path = os.path.join(DATASET_B_IMAGES, dup_file)

    label_name = os.path.splitext(dup_file)[0] + ".txt"
    label_path = os.path.join(DATASET_B_LABELS, label_name)

    if os.path.exists(image_path):
        os.remove(image_path)

    if os.path.exists(label_path):
        os.remove(label_path)

    deleted += 1

print("\n======================================")
print("Deletion Complete")
print("======================================")
print(f"Deleted Images : {deleted}")
print(f"Deleted Labels : {deleted}")

# ==========================================================
# SAVE REPORT
# ==========================================================

report_file = "duplicate_report.txt"

with open(report_file, "w") as f:

    f.write("Duplicate Removal Report\n")
    f.write("========================\n\n")

    f.write(f"Threshold: {HASH_THRESHOLD}\n\n")

    for dup, original, dist in duplicates:

        f.write(
            f"{dup} --> duplicate of {original} (distance={dist})\n"
        )

print(f"\nReport saved as: {report_file}")