import os
import smtplib
from email.message import EmailMessage

# 1. Configuration (Unga details-ah inga maathunga)
sender_email = "sender_mail@gmail.com"
sender_password = "password"
receiver_email = "receiver_mail@gmail.com"

# 2. Desktop File Path Setup
# Windows Desktop path ipdi thaan irukum. 'YOUR_WINDOWS_USERNAME'-ah mathidunga.
desktop_path = r"C:/Users/c2c.ITNT67/Desktop/1/message.txt"
file_name = os.path.basename(desktop_path) # report.txt-nu auto-va edukum

# 3. Email Object Configuration
msg = EmailMessage()
msg['Subject'] = "Desktop File Attachment From Python"
msg['From'] = sender_email
msg['To'] = receiver_email
msg.set_content("Hi, Enoda Desktop-la irunthu anupunatha file itho intha mail-la attached-ah iruku. Check panni paarunga!")

# 4. Reading and Attaching the File from Desktop
try:
    print(f"Reading file from Desktop: {file_name}...")
    # File-ah raw binary data-va ('rb') read panrom
    with open(desktop_path, 'rb') as f:
        file_data = f.read()
        
    # Mail-la file data-va sethu lock panrom
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
    print("File attached successfully!")

except FileNotFoundError:
    print(f"❌ Error: Desktop-la '{file_name}' nu entha file-um illa! Path-ah check pannunga.")
    exit()

# 5. Connect and Send via SMTP
try:
    print("Connecting to Gmail Server...")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure Connection
        server.login(sender_email, sender_password)
        print("Login Successful! Sending Mail...")
        
        server.send_message(msg)
        print(f"🎉 Mail with '{file_name}' sent successfully!")

except Exception as e:
    print(f"❌ Error occurred: {e}")
