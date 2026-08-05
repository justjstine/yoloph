import os

# Path to your labels folder
labels_folder = r"C:\Users\almad\Desktop\Thesis\Dataset\Segementation\Combined Dataset\train\labels"

total_labels = 0
non_potholes = 0
potholes = 0
missing_labels = 0

# Supported image extensions (optional if you also want to compare with images)
for file in os.listdir(labels_folder):
    if file.endswith(".txt"):
        total_labels += 1
        label_path = os.path.join(labels_folder, file)

        with open(label_path, "r") as f:
            content = f.read().strip()

        if content == "":
            non_potholes += 1
        else:
            potholes += 1

print("=" * 40)
print(f"Total Label Files : {total_labels}")
print(f"Pothole Images    : {potholes}")
print(f"Non-Pothole Images: {non_potholes}")
print("=" * 40)