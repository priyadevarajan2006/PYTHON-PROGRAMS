import datetime
import os
import smtplib
import time
from email.message import EmailMessage

# 1. Configuration (Set your details here)
sender_email = "sender_mail@gmail.com"
sender_password = "password"  # App password without spaces
receiver_email = "receiver_mail@gmail.com"

# 2. Desktop File Path Setup
desktop_path = r"C:/Users/c2c.ITNT67/Desktop/1/message.txt"
file_name = os.path.basename(desktop_path)

# 3. FIX YOUR TARGET TIME HERE (24-Hour Format -> HH:MM)
# For example: "15:30" for 3:30 PM, or "09:15" for 9:15 AM
target_time = "12:30"  

print(f"⏰ Scheduler Started! Waiting for the clock to strike {target_time}...")

# 4. Background Waiting Loop
while True:
    # Get the current system time in HH:MM format
    current_time = datetime.datetime.now().strftime("%H:%M")
    
    # Check if the current time matches your fixed target time
    if current_time == target_time:
        print(f"\n🎯 Time matched ({current_time})! Preparing to send email...")
        break  # Break out of the loop to send the mail
        
    # Wait for 30 seconds before checking the clock again (saves CPU power)
    print(f"Current time is {current_time}. Still waiting...", end="\r")
    time.sleep(30)

# 5. Build and Send the Email (Triggers only when time matches)
msg = EmailMessage()
msg['Subject'] = "Scheduled Desktop File Delivery"
msg['From'] = sender_email
msg['To'] = receiver_email
msg.set_content(f"Hi, this is an automated email triggered exactly at {target_time}.")

try:
    # Read the file
    with open(desktop_path, 'rb') as f:
        file_data = f.read()
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
    
    # SMTP Delivery
    print("Connecting to Gmail Server...")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        print(f"🎉 Success! Automated email with '{file_name}' sent at {target_time}!")

except FileNotFoundError:
    print(f"❌ Error: Could not find the file at {desktop_path}")
except Exception as e:
    print(f"❌ SMTP Error occurred: {e}")
