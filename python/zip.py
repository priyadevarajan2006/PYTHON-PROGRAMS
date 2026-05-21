import datetime
import os
import shutil  # Folder-ah ZIP-ah maatha intha library use aaguthu
import smtplib
import time
from email.message import EmailMessage

# 1. Configuration (Unga details-ah inga maathunga)
sender_email = "priyadevarajan2006@gmail.com"
sender_password = "lxcyzraxvqycollr"  # App password without spaces
receiver_email = "priyadevarajan2006@gmail.com"

# 2. Desktop FOLDER Path Setup
# Ungaloda target folder path matrum athu enna bera save aagunum-nu fix panrom
folder_to_send = r"C:/Users/c2c.ITNT67/Desktop/python"
zip_output_path = r"C:/Users/c2c.ITNT67/Desktop/python"
actual_zip_file = zip_output_path + ".zip"

# 3. TIME FIX (24-Hour Format -> HH:MM)
target_time = "12:50"  

print(f"⏰ Scheduler Started! Waiting for {target_time} to send the folder...")

# 4. Background Waiting Loop
while True:
    current_time = datetime.datetime.now().strftime("%H:%M")
    if current_time == target_time:
        print(f"\n🎯 Time matched ({current_time})! Processing folder...")
        break
    print(f"Current time is {current_time}. Waiting...", end="\r")
    time.sleep(30)

# 5. ZIPPING THE FOLDER
try:
    print(f"Zipping the folder '{os.path.basename(folder_to_send)}'...")
    # shutil.make_archive automatically compresses the whole folder into a single ZIP file
    shutil.make_archive(zip_output_path, 'zip', folder_to_send)
    print("Folder successfully compressed into ZIP!")
except FileNotFoundError:
    print(f"❌ Error: Desktop-la '{folder_to_send}' nu folder ethuvum illa!")
    exit()

# 6. EMAIL CONFIGURATION
msg = EmailMessage()
msg['Subject'] = "Automated Folder Delivery (ZIP Format)"
msg['From'] = sender_email
msg['To'] = receiver_email
msg.set_content(f"Hi, Enoda Desktop-la iruntha muzhu folder-um ZIP-ah convert aagi intha mail-la attached-ah iruku.")

# 7. READING THE ZIP & SENDING VIA SMTP
try:
    # ZIP file-ah read panrom
    with open(actual_zip_file, 'rb') as f:
        file_data = f.read()
    
    # Mail-la attach panrom
    msg.add_attachment(file_data, maintype='application', subtype='zip', filename=os.path.basename(actual_zip_file))
    
    # SMTP Process
    print("Connecting to Gmail Server...")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        print("Login Successful! Sending Mail...")
        server.send_message(msg)
        print(f"🎉 Success! Compressed folder sent successfully at {target_time}!")

    # Optional: Mail anupunathuku apram desktop-la uruvana ZIP file-ah delete panna intha line-ah use பண்ணலாம்
    # os.remove(actual_zip_file)

except Exception as e:
    print(f"❌ Error occurred: {e}")
