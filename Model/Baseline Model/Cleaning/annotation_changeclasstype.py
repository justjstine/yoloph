import os

# ============================================================
# LABEL FOLDERS
# ============================================================

label_folders = [
    r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\Thesis Potholes.yolov8\train\labels",
    r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\Thesis Potholes.yolov8\val\labels",
]


# ============================================================
# CONVERT CLASSES 1 AND 2 TO CLASS 0
# ============================================================

changed_files = 0
changed_labels = 0

for labels_folder in label_folders:

    print()
    print("=" * 60)
    print(f"Checking: {labels_folder}")
    print("=" * 60)

    for filename in os.listdir(labels_folder):

        if not filename.lower().endswith(".txt"):
            continue

        label_path = os.path.join(
            labels_folder,
            filename
        )

        with open(label_path, "r") as file:
            lines = file.readlines()

        new_lines = []
        file_changed = False

        for line in lines:

            parts = line.strip().split()

            if not parts:
                continue

            # Class ID
            if parts[0] in ["1", "2"]:

                parts[0] = "0"

                changed_labels += 1
                file_changed = True

            new_lines.append(" ".join(parts))

        if file_changed:

            with open(label_path, "w") as file:
                file.write("\n".join(new_lines) + "\n")

            changed_files += 1

            print(f"Changed: {filename}")


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 60)
print("DONE")
print("=" * 60)

print(f"Files changed : {changed_files}")
print(f"Labels changed: {changed_labels}")

print()
print("1 -> 0")
print("2 -> 0")
print("0 remains 0")
print("=" * 60)