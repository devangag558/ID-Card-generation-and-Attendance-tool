# ID Card Generation and Attendance Tool

## How to Use

### Initial Step 
if you are changing the file name of uploaded images according to roll number
`function renamePhotos() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const lastRow = sheet.getLastRow();
  
  // Starting at Row 2 to skip headers
  for (let i = 2; i <= lastRow; i++) {
    const rollNumber = sheet.getRange(i, 3).getValue(); // Column C
    const fileUrl = sheet.getRange(i, 6).getValue();   // Column F
    
    if (fileUrl && rollNumber) {
      try {
        // Extract the File ID from the URL
        const fileId = fileUrl.match(/[-\w]{25,}/);
        
        if (fileId) {
          const file = DriveApp.getFileById(fileId[0]);
          const extension = file.getName().split('.').pop(); // Keep original extension (jpg, png, etc.)
          
          // Rename the file
          file.setName(rollNumber + "." + extension);
          
          // Optional: Mark as "Done" in Column G to track progress
          sheet.getRange(i, 7).setValue("Renamed");
        }
      } catch (e) {
        console.log("Error at row " + i + ": " + e.toString());
        sheet.getRange(i, 7).setValue("Error: Not Found");
      }
    }
  }
}`

### Step 1 – Prepare the Excel File
Create an Excel/CSV file containing details of all participants for whom ID cards need to be generated.  
👉 The most efficient way is to circulate a Google Form and collect both participant details and photographs.

### Step 2 – Crop Participant Photos
Assign a unique ID to each participant (e.g., roll number) and run **`python image_cropper.py`**.  
This program helps you quickly crop photographs:  

- It automatically places a square box around the face.  
- You can adjust the box using arrow keys or draw a new one.  
- Press **Enter** to confirm and move on to the next photo.  
- You only need to select the folder containing all the photos.  

<img width="400" height="500" alt="image" src="https://github.com/user-attachments/assets/11aed34c-bb52-4171-b6e6-f6849d97afd5" />

### Step 3 – Generate QR Codes
Run **`qr.py`** to generate QR codes for the chosen fields from the CSV.  
You can also use the **`rounded_square.ipynb`** notebook to apply rounded corners to images if required.

### Step 4 – Design and Generate ID Cards
Run **`id_card_maker.py`**.  
This tool works like a lightweight Photoshop editor to help you place:  

- Participant name  
- QR code  
- Photograph  

onto the ID card template.  
It will then generate all ID cards into a separate folder and also export a combined **PDF file**, which is useful for printing.  

<img width="625" height="600" alt="image" src="https://github.com/user-attachments/assets/fd6bad9d-de8b-4afc-93be-050da892444a" />

### Step 5 – Attendance System
Install **Pydroid** (or any other relevant Python environment) on your Android phone and run **`Attendance_System.py`**.  
You will then see the mobile interface for attendance tracking.  

<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/ce54faf4-aabb-4e5e-a74a-a08f3aa29b23" width="250"></td>
    <td><img src="https://github.com/user-attachments/assets/a5ec2b82-a508-449a-9914-6d2d5c19b802" width="250"></td>
    <td><img src="https://github.com/user-attachments/assets/57b313bf-2eba-4136-8605-489585163e44" width="250"></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/b9878f8b-98cd-4167-9770-eee4867d912c" width="250"></td>
    <td><img src="https://github.com/user-attachments/assets/9e40dcc5-8a90-4ebc-ae0a-f089c05e9715" width="250"></td>
    <td><img src="https://github.com/user-attachments/assets/a25f97a1-6ddc-44ba-8925-b28509fbd98c" width="250"></td>
  </tr>
</table>
