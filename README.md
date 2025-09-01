# ID-Card-generation-and-Attendance-tool

## How to use

### Step 1 - prepare the excel of all the participants for which you have to make th ID cards (Most efficient way is to circulate the google form) along with the Photos 

### Step 2 - Give some unique id (Roll number in this case) and run "python image cropper.py"
This py program will help you crop the photgraphs very quickly as it will just move on to next on pressing enter, it already gives the square shaped box around face but you can shift it using the arrow keys or make entirely new one. You just have to select the folder which contains all the photos

<img width="400" height="500" alt="image" src="https://github.com/user-attachments/assets/11aed34c-bb52-4171-b6e6-f6849d97afd5" />


### Step 3 - Make the QR codes for the required feilds by executing the qr.py file
You could select which feild from the CSV you want to include in the QR code. You could use the "rounded square.ipynb" notebook to make the rounded corners for the image

### Step 4 - Now use "id card maker.py" file
This tool is basically the photoshop tool which helps you in placing name, QR code, and photo on the ID Card Template. This will generate all the ID Cards in the seperate folder and also will generate the PDF file which would be very helpful while printing the ID Cards

<img width="625" height="600" alt="image" src="https://github.com/user-attachments/assets/fd6bad9d-de8b-4afc-93be-050da892444a" />


### Step 5 - Download Pydroid or any other relevant software using which you can run "Attendance System.py" in the Android Phone and you would be able to see the interface

![WhatsApp Image 2025-09-01 at 13 55 44](https://github.com/user-attachments/assets/ce54faf4-aabb-4e5e-a74a-a08f3aa29b23)
![WhatsApp Image 2025-09-01 at 13 55 45](https://github.com/user-attachments/assets/a5ec2b82-a508-449a-9914-6d2d5c19b802)
![WhatsApp Image 2025-09-01 at 13 55 45 (1)](https://github.com/user-attachments/assets/57b313bf-2eba-4136-8605-489585163e44)
![WhatsApp Image 2025-09-01 at 13 55 46](https://github.com/user-attachments/assets/b9878f8b-98cd-4167-9770-eee4867d912c)
![WhatsApp Image 2025-09-01 at 13 55 46 (1)](https://github.com/user-attachments/assets/9e40dcc5-8a90-4ebc-ae0a-f089c05e9715)
![WhatsApp Image 2025-09-01 at 13 55 46 (2)](https://github.com/user-attachments/assets/a25f97a1-6ddc-44ba-8925-b28509fbd98c)
