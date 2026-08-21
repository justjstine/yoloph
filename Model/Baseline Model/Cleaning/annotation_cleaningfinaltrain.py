import os
import shutil


# ============================================================
# FOLDERS
# ============================================================

train_images = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\FINAL Dataset\train\images"

train_labels = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\FINAL Dataset\train\labels"


# ============================================================
# DESTINATION FOR TRAIN DUPLICATES
# ============================================================

duplicate_images = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\FINAL Dataset\train_dups\images"

duplicate_labels = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\FINAL Dataset\train_dups\labels"


# ============================================================
# DUPLICATE REPORT
# ============================================================

report_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "dataset_duplicate_report.txt"
)


# ============================================================
# CREATE DESTINATION FOLDERS
# ============================================================

os.makedirs(
    duplicate_images,
    exist_ok=True
)

os.makedirs(
    duplicate_labels,
    exist_ok=True
)


# ============================================================
# CHECK REPORT
# ============================================================

if not os.path.exists(report_path):

    print("=" * 70)
    print("ERROR: DUPLICATE REPORT NOT FOUND")
    print("=" * 70)

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
# VARIABLES
# ============================================================

distance_0_files = set()
distance_1_5_files = set()

current_distance = None
section = None


# ============================================================
# READ TRAIN ↔ TRAIN SECTION
# ============================================================

for line in lines:

    line = line.strip()


    # --------------------------------------------------------
    # FIND TRAIN ↔ TRAIN SECTION
    # --------------------------------------------------------

    if line == "TRAIN ↔ TRAIN DUPLICATES":

        section = "train_train"
        current_distance = None
        continue


    # --------------------------------------------------------
    # STOP WHEN NEXT SECTION STARTS
    # --------------------------------------------------------

    if line in [
        "VALID ↔ VALID DUPLICATES",
        "TRAIN ↔ VALID DUPLICATES"
    ]:

        section = None
        current_distance = None
        continue


    # --------------------------------------------------------
    # ONLY PROCESS TRAIN ↔ TRAIN
    # --------------------------------------------------------

    if section != "train_train":
        continue


    # --------------------------------------------------------
    # FIND DISTANCE
    # --------------------------------------------------------

    if line.startswith("[") and "Distance:" in line:

        try:

            distance_text = line.split(
                "Distance:",
                1
            )[1].strip()

            current_distance = int(
                distance_text
            )

        except:

            current_distance = None

        continue


    # --------------------------------------------------------
    # FIND IMAGE 1
    # --------------------------------------------------------

    if line.startswith("IMAGE 1:"):

        if current_distance is not None:

            filename = line.split(
                "IMAGE 1:",
                1
            )[1].strip()

            if filename:

                if current_distance == 0:

                    distance_0_files.add(
                        filename
                    )

                elif 1 <= current_distance <= 5:

                    distance_1_5_files.add(
                        filename
                    )


    # --------------------------------------------------------
    # FIND IMAGE 2
    # --------------------------------------------------------

    elif line.startswith("IMAGE 2:"):

        if current_distance is not None:

            filename = line.split(
                "IMAGE 2:",
                1
            )[1].strip()

            if filename:

                if current_distance == 0:

                    distance_0_files.add(
                        filename
                    )

                elif 1 <= current_distance <= 5:

                    distance_1_5_files.add(
                        filename
                    )


# ============================================================
# IMPORTANT
# ============================================================
#
# We don't want to move BOTH copies of an identical pair.
#
# For example:
#
# IMAGE 1: image001.jpg
# IMAGE 2: image002.jpg
# Distance: 0
#
# We need to keep ONE and move ONE.
#
# Therefore, we need to determine which file to move.
#
# ============================================================


# ============================================================
# FIND DISTANCE-0 PAIRS
# ============================================================

distance_0_pairs = []

current_distance = None
image_1 = None

section = None


for line in lines:

    line = line.strip()


    # --------------------------------------------------------
    # TRAIN ↔ TRAIN SECTION
    # --------------------------------------------------------

    if line == "TRAIN ↔ TRAIN DUPLICATES":

        section = "train_train"
        current_distance = None
        image_1 = None
        continue


    if line in [
        "VALID ↔ VALID DUPLICATES",
        "TRAIN ↔ VALID DUPLICATES"
    ]:

        section = None
        continue


    if section != "train_train":
        continue


    # --------------------------------------------------------
    # DISTANCE
    # --------------------------------------------------------

    if line.startswith("[") and "Distance:" in line:

        try:

            current_distance = int(
                line.split(
                    "Distance:",
                    1
                )[1].strip()
            )

        except:

            current_distance = None

        continue


    # --------------------------------------------------------
    # IMAGE 1
    # --------------------------------------------------------

    if line.startswith("IMAGE 1:"):

        image_1 = line.split(
            "IMAGE 1:",
            1
        )[1].strip()

        continue


    # --------------------------------------------------------
    # IMAGE 2
    # --------------------------------------------------------

    if line.startswith("IMAGE 2:"):

        image_2 = line.split(
            "IMAGE 2:",
            1
        )[1].strip()


        if current_distance == 0:

            if image_1 and image_2:

                distance_0_pairs.append(
                    (
                        image_1,
                        image_2
                    )
                )


# ============================================================
# DETERMINE WHICH DUPLICATE TO MOVE
# ============================================================

files_to_move = set()

kept_files = set()


for image_1, image_2 in distance_0_pairs:

    # If image 1 is already being kept,
    # move image 2.

    if image_1 in kept_files:

        files_to_move.add(
            image_2
        )

        continue


    # If image 2 is already being kept,
    # move image 1.

    if image_2 in kept_files:

        files_to_move.add(
            image_1
        )

        continue


    # Otherwise:
    # Keep IMAGE 1
    # Move IMAGE 2

    kept_files.add(
        image_1
    )

    files_to_move.add(
        image_2
    )


# ============================================================
# REMOVE ANY FILE THAT IS BEING KEPT
# ============================================================

files_to_move -= kept_files


# ============================================================
# DISPLAY RESULTS
# ============================================================

print()
print("=" * 70)
print("TRAIN ↔ TRAIN DUPLICATE CLEANING")
print("=" * 70)

print()

print(
    f"Distance 0 pairs      : "
    f"{len(distance_0_pairs)}"
)

print(
    f"Distance 0 files move : "
    f"{len(files_to_move)}"
)

print(
    f"Distance 1–5 files    : "
    f"{len(distance_1_5_files)}"
)

print()

print("RULES")
print("-" * 70)

print("Distance 0   → MOVE ONE DUPLICATE")
print("Distance 1–5 → REPORT ONLY")
print("Distance 6+  → IGNORE")
print()
print("VALID        → NOT MODIFIED")

print()
print("=" * 70)


# ============================================================
# ASK CONFIRMATION
# ============================================================

answer = input(
    "Move the distance-0 TRAIN duplicates? (yes/no): "
).strip().lower()


if answer != "yes":

    print()
    print("Operation cancelled.")

    input(
        "\nPress ENTER to exit..."
    )

    exit()


# ============================================================
# MOVE DISTANCE 0 DUPLICATES
# ============================================================

moved_images = 0
moved_labels = 0

missing_images = 0
missing_labels = 0


for filename in sorted(files_to_move):


    # ========================================================
    # IMAGE
    # ========================================================

    source_image = os.path.join(
        train_images,
        filename
    )

    destination_image = os.path.join(
        duplicate_images,
        filename
    )


    if os.path.exists(source_image):

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
        train_labels,
        label_filename
    )

    destination_label = os.path.join(
        duplicate_labels,
        label_filename
    )


    if os.path.exists(source_label):

        if os.path.exists(destination_label):

            print(
                f"ALREADY EXISTS LABEL: "
                f"{label_filename}"
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
            f"LABEL NOT FOUND: "
            f"{label_filename}"
        )


# ============================================================
# FINAL REPORT
# ============================================================

print()
print("=" * 70)
print("TRAIN ↔ TRAIN CLEANING COMPLETE")
print("=" * 70)

print()

print(
    f"Distance 0 pairs       : "
    f"{len(distance_0_pairs)}"
)

print(
    f"Images moved            : "
    f"{moved_images}"
)

print(
    f"Labels moved            : "
    f"{moved_labels}"
)

print(
    f"Images missing          : "
    f"{missing_images}"
)

print(
    f"Labels missing          : "
    f"{missing_labels}"
)

print()

print(
    f"Distance 1–5 reported   : "
    f"{len(distance_1_5_files)}"
)

print()

print("Moved images:")
print(duplicate_images)

print()

print("Moved labels:")
print(duplicate_labels)

print()
print("=" * 70)
print("IMPORTANT")
print("=" * 70)

print("Distance 0   → MOVED")
print("Distance 1–5 → NOT MOVED")
print("Distance 6+  → KEPT")
print("VALID        → NOT MODIFIED")

print("=" * 70)

input(
    "\nPress ENTER to exit..."
)