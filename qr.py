# import pandas as pd
# import qrcode
# from PIL import Image
# import os

# # Path to your CSV file
# CSV_FILE = r'SG ID CARDS/ID Card - Form Responses 1.csv'  # change this to your actual file path

# # Output folder
# OUTPUT_FOLDER = 'newQR'
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# # Load the CSV
# df = pd.read_csv(CSV_FILE)

# # Iterate over each row
# for index, row in df.iterrows():
#     roll = str(row['Roll Number']).strip()
#     name = str(row['Name']).strip().title()
#     degree = str(row['Degree']).strip()
#     department = str(row['Dept.']).strip()

#     # QR data as a string
#     qr_data = f"{roll},{name},{degree},{department}"

#     # Generate QR Code
#     qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
#     qr.add_data(qr_data)
#     qr.make(fit=True)
    
#     img = qr.make_image(fill_color="black", back_color="white").convert("RGB")


#     # Save QR code
#     img.save(os.path.join(OUTPUT_FOLDER, f"qr_{roll}.png"))

# print("✅ QR codes generated in 'qr_codes' folder.")


import pandas as pd
import qrcode
from PIL import Image
import os

# Path to your CSV file
CSV_FILE = r'SG ID CARDS/ID Card - Form Responses 1.csv'

# Output folder
OUTPUT_FOLDER = 'newQR3'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load the CSV
df = pd.read_csv(CSV_FILE)

# Iterate over each row
for index, row in df.iterrows():
    roll = str(row['Roll Number']).strip()
    name = str(row['Name']).strip().title()
    degree = str(row['Degree']).strip()
    department = str(row['Dept.']).strip()

    # QR data as a string
    qr_data = f"{roll},{name},{degree},{department}"

    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,  # Let QRCode determine version
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  # Initial size (will be resized later)
        border=2
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#05042b", back_color="white").convert("RGB")

    # Resize to 300x300
    img = img.resize((150, 150), Image.LANCZOS)

    # Save QR code
    img.save(os.path.join(OUTPUT_FOLDER, f"qr_{roll}.png"))

print("✅ QR codes generated with fixed size 300x300 in 'newQR' folder.")
