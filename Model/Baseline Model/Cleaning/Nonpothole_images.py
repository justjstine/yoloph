import os

labels_folder = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\Thesis Potholes 2.yolov8\train\labels"
images_folder = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\Thesis Potholes 2.yolov8\train\images"

extensions = [".jpg", ".jpeg", ".png"]

non_pothole_images = []

for file in os.listdir(labels_folder):
    if not file.endswith(".txt"):
        continue

    label_path = os.path.join(labels_folder, file)

    with open(label_path, "r") as f:
        content = f.read().strip()

    if content == "":
        base = os.path.splitext(file)[0]

        for ext in extensions:
            image_path = os.path.join(images_folder, base + ext)
            if os.path.exists(image_path):
                non_pothole_images.append(image_path)
                break

print(f"Total Non-Pothole Images: {len(non_pothole_images)}")
print("-" * 50)

for image in non_pothole_images:
    print(image)