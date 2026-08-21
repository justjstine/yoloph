import os
import shutil


# ============================================================
# FOLDERS
# ============================================================

# VALIDATION IMAGES
valid_images = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\Kaggle\val\images"

# VALIDATION LABELS
valid_labels = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\Kaggle\val\labels"

# DESTINATION FOR DUPLICATE IMAGES
duplicate_images = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\Kaggle\val_dups\images"

# DESTINATION FOR DUPLICATE LABELS
duplicate_labels = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\Kaggle\val_dups\labels"


# ============================================================
# REPORT
# ============================================================

report_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "train_valid_near_duplicate_report.txt"
)


# ============================================================
# CREATE DESTINATION FOLDERS
# ============================================================

os.makedirs(duplicate_images, exist_ok=True)
os.makedirs(duplicate_labels, exist_ok=True)


# ============================================================
# CHECK REPORT
# ============================================================

if not os.path.exists(report_path):

    print("ERROR: Report file was not found.")

    print()
    print("Expected report:")
    print(report_path)

    input("\nPress ENTER to exit...")
    exit()


# ============================================================
# READ REPORT
# ============================================================

with open(
    report_path,
    "r",
    encoding="utf-8"
) as report:

    lines = report.readlines()


# ============================================================
# FIND DISTANCE 0–5 VALID IMAGES
# ============================================================

files_to_move = []

current_distance = None

for line in lines:

    line = line.strip()

    # --------------------------------------------------------
    # DISTANCE
    # --------------------------------------------------------

    if line.startswith("Distance :"):

        try:
            current_distance = int(
                line.split(":", 1)[1].strip()
            )

        except ValueError:
            current_distance = None


    # --------------------------------------------------------
    # VALID IMAGE
    # --------------------------------------------------------

    elif line.startswith("VALID    :"):

        if current_distance is not None:

            if 0 <= current_distance <= 5:

                filename = line.split(
                    ":",
                    1
                )[1].strip()

                if filename:
                    files_to_move.append(filename)


# Remove duplicate filenames
files_to_move = list(
    dict.fromkeys(files_to_move)
)


# ============================================================
# DISPLAY INFORMATION
# ============================================================

print("=" * 70)
print("TRAIN vs VALID DUPLICATE MOVING")
print("=" * 70)

print()
print("Distance 0–5 will be moved.")
print("Distance 6+ will remain.")
print()
print("TRAIN will NOT be modified.")
print()

print(
    f"Validation images to move: "
    f"{len(files_to_move)}"
)

print()
print("=" * 70)


# ============================================================
# ASK FOR CONFIRMATION
# ============================================================

answer = input(
    "\nAre you sure you want to move these files? "
    "(yes/no): "
).strip().lower()


if answer != "yes":

    print()
    print("Operation cancelled.")
    input("\nPress ENTER to exit...")
    exit()


# ============================================================
# MOVE FILES
# ============================================================

moved_images = 0
moved_labels = 0

missing_images = 0
missing_labels = 0


for filename in files_to_move:

    # ========================================================
    # IMAGE
    # ========================================================

    source_image = os.path.join(
        valid_images,
        filename
    )

    destination_image = os.path.join(
        duplicate_images,
        filename
    )


    if os.path.exists(source_image):

        # Prevent overwriting an existing file
        if os.path.exists(destination_image):

            print(
                f"ALREADY EXISTS: {filename}"
            )

        else:

            shutil.move(
                source_image,
                destination_image
            )

            moved_images += 1

            print(
                f"MOVED IMAGE: {filename}"
            )

    else:

        missing_images += 1

        print(
            f"IMAGE NOT FOUND: {filename}"
        )


    # ========================================================
    # LABEL
    # ========================================================

    label_filename = (
        os.path.splitext(filename)[0]
        + ".txt"
    )


    source_label = os.path.join(
        valid_labels,
        label_filename
    )

    destination_label = os.path.join(
        duplicate_labels,
        label_filename
    )


    if os.path.exists(source_label):

        # Prevent overwriting
        if os.path.exists(destination_label):

            print(
                f"ALREADY EXISTS: {label_filename}"
            )

        else:

            shutil.move(
                source_label,
                destination_label
            )

            moved_labels += 1

            print(
                f"MOVED LABEL: {label_filename}"
            )

    else:

        missing_labels += 1

        print(
            f"LABEL NOT FOUND: {label_filename}"
        )


# ============================================================
# FINAL SUMMARY
# ============================================================

print()
print("=" * 70)
print("MOVING COMPLETE")
print("=" * 70)

print()
print(
    f"Images detected in report : "
    f"{len(files_to_move)}"
)

print(
    f"Images moved              : "
    f"{moved_images}"
)

print(
    f"Labels moved              : "
    f"{moved_labels}"
)

print(
    f"Images not found          : "
    f"{missing_images}"
)

print(
    f"Labels not found          : "
    f"{missing_labels}"
)

print()
print("Images destination:")
print(duplicate_images)

print()
print("Labels destination:")
print(duplicate_labels)

print()
print("=" * 70)
print("IMPORTANT")
print("=" * 70)

print("Distance 0–5: MOVED")
print("Distance 6+:  KEPT")
print("TRAIN:        NOT MODIFIED")

print("=" * 70)

input("\nPress ENTER to exit...")