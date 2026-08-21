import os
from PIL import Image
import imagehash
from datetime import datetime


# ============================================================
# FOLDERS
# ============================================================

train_folder = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\FINAL Dataset\train\images"

valid_folder = r"C:\Users\almad\OneDrive\Desktop\Thesis\Final Version\FINAL Dataset\val\images"


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

# 0     = identical pHash
# 1-5   = very similar
# 6+    = less similar

threshold = 5


# ============================================================
# FUNCTION: CREATE HASHES
# ============================================================

def create_hashes(folder):

    hashes = {}
    errors = []

    if not os.path.exists(folder):

        print("Folder not found:")
        print(folder)

        return hashes, errors

    for filename in os.listdir(folder):

        if not filename.lower().endswith(image_extensions):
            continue

        path = os.path.join(
            folder,
            filename
        )

        try:

            image = Image.open(path)

            hashes[filename] = imagehash.phash(image)

        except Exception as e:

            errors.append(
                f"{filename} | {e}"
            )

    return hashes, errors


# ============================================================
# CREATE TRAIN HASHES
# ============================================================

print("=" * 70)
print("CREATING TRAIN HASHES")
print("=" * 70)

train_hashes, train_errors = create_hashes(
    train_folder
)

print(
    f"Train images checked: "
    f"{len(train_hashes)}"
)


# ============================================================
# CREATE VALID HASHES
# ============================================================

print()
print("=" * 70)
print("CREATING VALID HASHES")
print("=" * 70)

valid_hashes, valid_errors = create_hashes(
    valid_folder
)

print(
    f"Valid images checked: "
    f"{len(valid_hashes)}"
)


# ============================================================
# RESULTS
# ============================================================

train_duplicates = []
valid_duplicates = []
train_valid_duplicates = []


# ============================================================
# TRAIN ↔ TRAIN
# ============================================================

print()
print("=" * 70)
print("CHECKING TRAIN ↔ TRAIN")
print("=" * 70)

train_images = list(train_hashes.items())

for i in range(len(train_images)):

    image1, hash1 = train_images[i]

    for j in range(i + 1, len(train_images)):

        image2, hash2 = train_images[j]

        distance = hash1 - hash2

        if distance <= threshold:

            train_duplicates.append(
                (
                    image1,
                    image2,
                    distance
                )
            )

print(
    f"Potential TRAIN duplicates: "
    f"{len(train_duplicates)}"
)


# ============================================================
# VALID ↔ VALID
# ============================================================

print()
print("=" * 70)
print("CHECKING VALID ↔ VALID")
print("=" * 70)

valid_images = list(valid_hashes.items())

for i in range(len(valid_images)):

    image1, hash1 = valid_images[i]

    for j in range(i + 1, len(valid_images)):

        image2, hash2 = valid_images[j]

        distance = hash1 - hash2

        if distance <= threshold:

            valid_duplicates.append(
                (
                    image1,
                    image2,
                    distance
                )
            )

print(
    f"Potential VALID duplicates: "
    f"{len(valid_duplicates)}"
)


# ============================================================
# TRAIN ↔ VALID
# ============================================================

print()
print("=" * 70)
print("CHECKING TRAIN ↔ VALID")
print("=" * 70)

for train_image, train_hash in train_hashes.items():

    for valid_image, valid_hash in valid_hashes.items():

        distance = train_hash - valid_hash

        if distance <= threshold:

            train_valid_duplicates.append(
                (
                    train_image,
                    valid_image,
                    distance
                )
            )

print(
    f"Potential TRAIN ↔ VALID duplicates: "
    f"{len(train_valid_duplicates)}"
)


# ============================================================
# SORT RESULTS
# ============================================================

train_duplicates.sort(
    key=lambda x: x[2]
)

valid_duplicates.sort(
    key=lambda x: x[2]
)

train_valid_duplicates.sort(
    key=lambda x: x[2]
)


# ============================================================
# CREATE REPORT
# ============================================================

script_folder = os.path.dirname(
    os.path.abspath(__file__)
)

report_path = os.path.join(
    script_folder,
    "dataset_duplicate_report.txt"
)


with open(
    report_path,
    "w",
    encoding="utf-8"
) as report:

    report.write("=" * 70 + "\n")
    report.write("DATASET DUPLICATE CHECK REPORT\n")
    report.write("=" * 70 + "\n\n")

    report.write(
        f"Date: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    )


    # ========================================================
    # DATASET INFORMATION
    # ========================================================

    report.write("## DATASET\n\n")

    report.write(
        f"Train:\n{train_folder}\n\n"
    )

    report.write(
        f"Valid:\n{valid_folder}\n\n"
    )

    report.write(
        f"Train images checked: "
        f"{len(train_hashes)}\n"
    )

    report.write(
        f"Valid images checked: "
        f"{len(valid_hashes)}\n"
    )

    report.write(
        f"Threshold: "
        f"{threshold}\n\n"
    )


    # ========================================================
    # SUMMARY
    # ========================================================

    report.write("## RESULTS\n\n")

    report.write(
        f"TRAIN ↔ TRAIN duplicates: "
        f"{len(train_duplicates)}\n"
    )

    report.write(
        f"VALID ↔ VALID duplicates: "
        f"{len(valid_duplicates)}\n"
    )

    report.write(
        f"TRAIN ↔ VALID duplicates: "
        f"{len(train_valid_duplicates)}\n\n"
    )


    # ========================================================
    # DISTANCE GUIDE
    # ========================================================

    report.write("## DISTANCE GUIDE\n\n")

    report.write(
        "0     = identical pHash\n"
    )

    report.write(
        "1-5   = very similar; manually inspect\n"
    )

    report.write(
        "6-10  = potentially similar\n"
    )

    report.write(
        ">10   = generally different\n\n"
    )


    # ========================================================
    # TRAIN ↔ TRAIN
    # ========================================================

    report.write(
        "============================================================\n"
    )

    report.write(
        "TRAIN ↔ TRAIN DUPLICATES\n"
    )

    report.write(
        "============================================================\n\n"
    )

    if train_duplicates:

        for i, (
            image1,
            image2,
            distance
        ) in enumerate(
            train_duplicates,
            1
        ):

            path1 = os.path.abspath(
                os.path.join(
                    train_folder,
                    image1
                )
            )

            path2 = os.path.abspath(
                os.path.join(
                    train_folder,
                    image2
                )
            )

            report.write(
                f"[{i}] Distance: {distance}\n"
            )

            report.write(
                f"IMAGE 1: {image1}\n"
            )

            report.write(
                f"PATH 1 : {path1}\n"
            )

            report.write(
                f"IMAGE 2: {image2}\n"
            )

            report.write(
                f"PATH 2 : {path2}\n"
            )

            report.write(
                "-" * 60 + "\n"
            )

    else:

        report.write(
            "No potential TRAIN duplicates found.\n"
        )


    # ========================================================
    # VALID ↔ VALID
    # ========================================================

    report.write("\n")

    report.write(
        "============================================================\n"
    )

    report.write(
        "VALID ↔ VALID DUPLICATES\n"
    )

    report.write(
        "============================================================\n\n"
    )

    if valid_duplicates:

        for i, (
            image1,
            image2,
            distance
        ) in enumerate(
            valid_duplicates,
            1
        ):

            path1 = os.path.abspath(
                os.path.join(
                    valid_folder,
                    image1
                )
            )

            path2 = os.path.abspath(
                os.path.join(
                    valid_folder,
                    image2
                )
            )

            report.write(
                f"[{i}] Distance: {distance}\n"
            )

            report.write(
                f"IMAGE 1: {image1}\n"
            )

            report.write(
                f"PATH 1 : {path1}\n"
            )

            report.write(
                f"IMAGE 2: {image2}\n"
            )

            report.write(
                f"PATH 2 : {path2}\n"
            )

            report.write(
                "-" * 60 + "\n"
            )

    else:

        report.write(
            "No potential VALID duplicates found.\n"
        )


    # ========================================================
    # TRAIN ↔ VALID
    # ========================================================

    report.write("\n")

    report.write(
        "============================================================\n"
    )

    report.write(
        "TRAIN ↔ VALID DUPLICATES\n"
    )

    report.write(
        "============================================================\n\n"
    )

    if train_valid_duplicates:

        for i, (
            train_image,
            valid_image,
            distance
        ) in enumerate(
            train_valid_duplicates,
            1
        ):

            train_path = os.path.abspath(
                os.path.join(
                    train_folder,
                    train_image
                )
            )

            valid_path = os.path.abspath(
                os.path.join(
                    valid_folder,
                    valid_image
                )
            )

            report.write(
                f"[{i}] Distance: {distance}\n"
            )

            report.write(
                f"TRAIN IMAGE: {train_image}\n"
            )

            report.write(
                f"TRAIN PATH : {train_path}\n"
            )

            report.write(
                f"VALID IMAGE: {valid_image}\n"
            )

            report.write(
                f"VALID PATH : {valid_path}\n"
            )

            report.write(
                "-" * 60 + "\n"
            )

    else:

        report.write(
            "No potential TRAIN ↔ VALID duplicates found.\n"
        )


    # ========================================================
    # ERRORS
    # ========================================================

    if train_errors or valid_errors:

        report.write("\n")
        report.write(
            "## FILE ERRORS\n\n"
        )

        for error in train_errors:

            report.write(
                f"TRAIN | {error}\n"
            )

        for error in valid_errors:

            report.write(
                f"VALID | {error}\n"
            )


    report.write("\n")
    report.write("=" * 70 + "\n")
    report.write("END OF REPORT\n")
    report.write("=" * 70 + "\n")


# ============================================================
# TERMINAL SUMMARY
# ============================================================

print()
print("=" * 70)
print("DUPLICATE CHECK COMPLETE")
print("=" * 70)

print()
print(
    f"TRAIN ↔ TRAIN : "
    f"{len(train_duplicates)}"
)

print(
    f"VALID ↔ VALID : "
    f"{len(valid_duplicates)}"
)

print(
    f"TRAIN ↔ VALID : "
    f"{len(train_valid_duplicates)}"
)

print()
print("Report saved to:")
print(report_path)

print()
print("=" * 70)