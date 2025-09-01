import os
from PIL import Image

# Input and output folders
INPUT_FOLDER = "newQR"     # change this to your source folder
OUTPUT_FOLDER = "newQR2"  # change this to your target folder

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Supported image extensions
valid_exts = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")

# Resize all valid images
for filename in os.listdir(INPUT_FOLDER):
    if filename.lower().endswith(valid_exts):
        input_path = os.path.join(INPUT_FOLDER, filename)
        output_path = os.path.join(OUTPUT_FOLDER, filename)

        try:
            img = Image.open(input_path).convert("RGB")
            img = img.resize((150, 150), Image.LANCZOS)
            img.save(output_path)
            print(f"✅ Resized: {filename}")
        except Exception as e:
            print(f"❌ Failed: {filename} ({e})")

print("🎉 Done resizing all images to 250x250.")
