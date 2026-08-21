import os
import shutil


# ============================================================
# FOLDERS
# ============================================================

valid_images = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\FINAL Dataset\val\images"

valid_labels = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\FINAL Dataset\val\labels"


# ============================================================
# DUPLICATE DESTINATION
# ============================================================

duplicate_images = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\FINAL Dataset\val_dups\images"

duplicate_labels = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\FINAL Dataset\val_dups\labels"


# ============================================================
# REPORT
# ============================================================

report_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "dataset_duplicate_report.txt"
)


# ============================================================
# SETTINGS
# ============================================================

# Move distances 0 through 5
MAX_DISTANCE = 5


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
    print("ERROR: REPORT NOT FOUND")
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

valid_valid_files = set()
train_valid_files = set()

current_distance = None

section = None


# ============================================================
# READ DUPLICATES FROM REPORT
# ============================================================

for line in lines:

    line = line.strip()


    # --------------------------------------------------------
    # DETECT SECTION
    # --------------------------------------------------------

    if line == "VALID ↔ VALID DUPLICATES":

        section = "valid_valid"
        current_distance = None
        continue


    if line == "TRAIN ↔ VALID DUPLICATES":

        section = "train_valid"
        current_distance = None
        continue


    # --------------------------------------------------------
    # DETECT DISTANCE
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
    # VALID ↔ VALID
    # --------------------------------------------------------

    if section == "valid_valid":

        if line.startswith("IMAGE 1:"):

            if current_distance is not None:

                if current_distance <= MAX_DISTANCE:

                    filename = line.split(
                        "IMAGE 1:",
                        1
                    )[1].strip()

                    if filename:

                        valid_valid_files.add(
                            filename
                        )


        elif line.startswith("IMAGE 2:"):

            if current_distance is not None:

                if current_distance <= MAX_DISTANCE:

                    filename = line.split(
                        "IMAGE 2:",
                        1
                    )[1].strip()

                    if filename:

                        valid_valid_files.add(
                            filename
                        )


    # --------------------------------------------------------
    # TRAIN ↔ VALID
    # --------------------------------------------------------

    elif section == "train_valid":

        if line.startswith("VALID IMAGE:"):

            if current_distance is not None:

                if current_distance <= MAX_DISTANCE:

                    filename = line.split(
                        "VALID IMAGE:",
                        1
                    )[1].strip()

                    if filename:

                        train_valid_files.add(
                            filename
                        )


# ============================================================
# COMBINE FILES
# ============================================================

# VALID ↔ VALID gets priority first.
#
# If an image is already going to be moved because
# of VALID ↔ VALID, it does not need to be moved again.

all_files = (
    valid_valid_files |
    train_valid_files
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print()
print("=" * 70)
print("VALIDATION DUPLICATE CLEANING")
print("=" * 70)

print()

print(
    f"VALID ↔ VALID duplicate images : "
    f"{len(valid_valid_files)}"
)

print(
    f"TRAIN ↔ VALID duplicate images : "
    f"{len(train_valid_files)}"
)

print(
    f"TOTAL UNIQUE VALID IMAGES      : "
    f"{len(all_files)}"
)

print()

print(
    f"Distance 0-{MAX_DISTANCE} will be moved."
)

print(
    "TRAIN images will NOT be modified."
)

print()

print("=" * 70)


# ============================================================
# SHOW SOME FILES
# ============================================================

print()
print("FIRST 20 FILES TO BE MOVED:")
print("-" * 70)

for i, filename in enumerate(
    sorted(all_files),
    1
):

    print(
        f"{i}. {filename}"
    )

    if i >= 20:
        break


# ============================================================
# CONFIRMATION
# ============================================================

print()
print("=" * 70)

answer = input(
    "Move these validation images and labels? (yes/no): "
).strip().lower()


if answer != "yes":

    print()
    print("Operation cancelled.")

    input(
        "\nPress ENTER to exit..."
    )

    exit()


# ============================================================
# MOVE FILES
# ============================================================

moved_images = 0
moved_labels = 0

missing_images = 0
missing_labels = 0

already_moved = 0


for filename in sorted(all_files):


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

        if os.path.exists(destination_image):

            print(
                f"ALREADY EXISTS: {filename}"
            )

            already_moved += 1

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
# FINAL SUMMARY
# ============================================================

print()
print("=" * 70)
print("CLEANING COMPLETE")
print("=" * 70)

print()

print(
    f"VALID ↔ VALID unique images : "
    f"{len(valid_valid_files)}"
)

print(
    f"TRAIN ↔ VALID unique images : "
    f"{len(train_valid_files)}"
)

print(
    f"TOTAL UNIQUE IMAGES         : "
    f"{len(all_files)}"
)

print()

print(
    f"Images moved : "
    f"{moved_images}"
)

print(
    f"Labels moved : "
    f"{moved_labels}"
)

print(
    f"Images missing : "
    f"{missing_images}"
)

print(
    f"Labels missing : "
    f"{missing_labels}"
)

print()

print("Duplicate images:")
print(duplicate_images)

print()

print("Duplicate labels:")
print(duplicate_labels)

print()

print("=" * 70)
print("TRAIN WAS NOT MODIFIED")
print("=" * 70)

input(
    "\nPress ENTER to exit..."
)