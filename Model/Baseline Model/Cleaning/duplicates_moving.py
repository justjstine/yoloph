import os
from PIL import Image
import imagehash
from datetime import datetime


# ============================================================
# FOLDERS
# ============================================================

train_folder = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\Kaggle\train\images"

valid_folder = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\Kaggle\val\images"


# ============================================================
# SETTINGS
# ============================================================

image_extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
)

# 0 = identical
# 1-5 = very similar
threshold = 5


# ============================================================
# VARIABLES
# ============================================================

train_hashes = {}

train_count = 0
valid_count = 0

errors = []


# ============================================================
# CREATE TRAIN HASHES
# ============================================================

print("=" * 70)
print("CREATING TRAIN IMAGE HASHES")
print("=" * 70)

for filename in os.listdir(train_folder):

    if not filename.lower().endswith(image_extensions):
        continue

    train_count += 1

    path = os.path.join(
        train_folder,
        filename
    )

    try:

        image = Image.open(path)

        train_hashes[filename] = imagehash.phash(
            image
        )

    except Exception as e:

        errors.append(
            f"TRAIN | {filename} | {e}"
        )


print()
print(
    f"Train images checked : {train_count}"
)

print(
    f"Train images hashed  : {len(train_hashes)}"
)


# ============================================================
# COMPARE VALID AGAINST TRAIN
# ============================================================

print()
print("=" * 70)
print("CHECKING VALIDATION AGAINST TRAIN")
print("=" * 70)

near_duplicates = []


for filename in os.listdir(valid_folder):

    if not filename.lower().endswith(image_extensions):
        continue

    valid_count += 1

    valid_path = os.path.join(
        valid_folder,
        filename
    )

    try:

        image = Image.open(valid_path)

        valid_hash = imagehash.phash(
            image
        )

        for train_filename, train_hash in train_hashes.items():

            distance = valid_hash - train_hash

            # ------------------------------------------------
            # DISTANCE 0–5
            # ------------------------------------------------

            if 0 <= distance <= threshold:

                train_path = os.path.abspath(
                    os.path.join(
                        train_folder,
                        train_filename
                    )
                )

                valid_path_absolute = os.path.abspath(
                    valid_path
                )

                near_duplicates.append(
                    (
                        train_filename,
                        filename,
                        distance,
                        train_path,
                        valid_path_absolute
                    )
                )

    except Exception as e:

        errors.append(
            f"VALID | {filename} | {e}"
        )


# ============================================================
# SORT
# ============================================================

near_duplicates.sort(
    key=lambda x: x[2]
)


# ============================================================
# COUNT UNIQUE VALID IMAGES
# ============================================================

unique_valid_duplicates = set()

for (
    train_image,
    valid_image,
    distance,
    train_path,
    valid_path
) in near_duplicates:

    unique_valid_duplicates.add(
        valid_image
    )


# ============================================================
# CREATE REPORT
# ============================================================

script_folder = os.path.dirname(
    os.path.abspath(__file__)
)

report_path = os.path.join(
    script_folder,
    "train_valid_near_duplicate_report.txt"
)


with open(
    report_path,
    "w",
    encoding="utf-8"
) as report:

    # ========================================================
    # HEADER
    # ========================================================

    report.write(
        "=" * 80 + "\n"
    )

    report.write(
        "TRAIN vs VALID NEAR-DUPLICATE REPORT\n"
    )

    report.write(
        "=" * 80 + "\n\n"
    )

    report.write(
        f"Date: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    )


    # ========================================================
    # DATASET
    # ========================================================

    report.write(
        "## DATASET\n\n"
    )

    report.write(
        f"Train: {train_folder}\n"
    )

    report.write(
        f"Valid: {valid_folder}\n\n"
    )

    report.write(
        f"Train images checked: {train_count}\n"
    )

    report.write(
        f"Valid images checked: {valid_count}\n"
    )

    report.write(
        f"Threshold: {threshold}\n\n"
    )


    # ========================================================
    # RESULTS
    # ========================================================

    report.write(
        "## RESULTS\n\n"
    )

    report.write(
        f"Potential duplicate pairs: "
        f"{len(near_duplicates)}\n"
    )

    report.write(
        f"Unique validation images: "
        f"{len(unique_valid_duplicates)}\n\n"
    )


    # ========================================================
    # DISTANCE GUIDE
    # ========================================================

    report.write(
        "## DISTANCE GUIDE\n\n"
    )

    report.write(
        "0     = identical pHash\n"
    )

    report.write(
        "1-5   = very similar\n"
    )

    report.write(
        "6-10  = potentially similar\n"
    )

    report.write(
        "> 10  = generally different\n\n"
    )


    # ========================================================
    # DUPLICATE DETAILS
    # ========================================================

    report.write(
        "## DUPLICATE DETAILS\n\n"
    )

    if near_duplicates:

        for i, (
            train_image,
            valid_image,
            distance,
            train_path,
            valid_path
        ) in enumerate(
            near_duplicates,
            1
        ):

            report.write(
                f"[{i}]\n"
            )

            report.write(
                f"TRAIN    : {train_image}\n"
            )

            report.write(
                f"VALID    : {valid_image}\n"
            )

            report.write(
                f"Distance : {distance}\n"
            )

            report.write(
                f"TRAIN PATH:\n"
                f"{train_path}\n"
            )

            report.write(
                f"VALID PATH:\n"
                f"{valid_path}\n"
            )

            report.write(
                "-" * 70 + "\n"
            )

    else:

        report.write(
            "NO DUPLICATES FOUND.\n"
        )


    # ========================================================
    # ERRORS
    # ========================================================

    if errors:

        report.write(
            "\n## FILE ERRORS\n\n"
        )

        for error in errors:

            report.write(
                error + "\n"
            )


    # ========================================================
    # END
    # ========================================================

    report.write(
        "\n" + "=" * 80 + "\n"
    )

    report.write(
        "END OF REPORT\n"
    )

    report.write(
        "=" * 80 + "\n"
    )


# ============================================================
# TERMINAL SUMMARY
# ============================================================

print()
print("=" * 70)
print("DUPLICATE CHECK COMPLETE")
print("=" * 70)

print(
    f"Train images checked       : {train_count}"
)

print(
    f"Valid images checked       : {valid_count}"
)

print(
    f"Duplicate pairs            : "
    f"{len(near_duplicates)}"
)

print(
    f"Unique valid duplicates    : "
    f"{len(unique_valid_duplicates)}"
)

print()
print("Report saved to:")
print(report_path)

print()
print("=" * 70)