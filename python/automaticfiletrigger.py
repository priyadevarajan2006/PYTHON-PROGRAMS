import datetime
import os
import shutil
import smtplib
import time
from email.message import EmailMessage

sender_email = "sender_mail@gmail.com"
sender_password = "password"  
receiver_email = "receiver_mail@gmail.com"

source_folder = r"C:\Users\c2c.ITNT67\Desktop\python"

temp_sync_folder = r"C:\Users\c2c.ITNT67\Desktop\python\today_updates"

zip_output_path = r"C:\Users\c2c.ITNT67\Desktop\python\today_updates_compressed"
actual_zip_file = zip_output_path + ".zip"

target_time = "14:49"  

print(f"⏰ Automated Daily ZIP Sync Started! Waiting for {target_time}...")

while True:
    current_time = datetime.datetime.now().strftime("%H:%M")
    if current_time == target_time:
        print(f"\n🎯 Time matched ({current_time})! Checking for today's files...")
        
       
        if os.path.exists(temp_sync_folder):
            shutil.rmtree(temp_sync_folder)
        if os.path.exists(actual_zip_file):
            os.remove(actual_zip_file)
            
        today_updated_files = []
        current_timestamp = time.time()
        one_day_seconds = 24 * 60 * 60  
        
        try:
            for file_name in os.listdir(source_folder):
                full_file_path = os.path.join(source_folder, file_name)
                
                if os.path.isfile(full_file_path):
                    file_modified_time = os.path.getmtime(full_file_path)
                    
                    if (current_timestamp - file_modified_time) <= one_day_seconds:
                        today_updated_files.append(full_file_path)
        except FileNotFoundError:
            print(f"❌ Error: Source folder missing -> {source_folder}")
            time.sleep(60)
            continue

        if not today_updated_files:
            print("ℹ️ No new files updated in the last 24 hours. Skipping mail.")
        else:
            print(f"📋 Found {len(today_updated_files)} updated files. Creating temporary ZIP archive...")
            
            os.makedirs(temp_sync_folder)
            for file_path in today_updated_files:
                shutil.copy(file_path, temp_sync_folder)
        
            shutil.make_archive(zip_output_path, 'zip', temp_sync_folder)
            print("📦 ZIP file created successfully!")

            msg = EmailMessage()
            msg['Subject'] = f"Daily Particular ZIP Update - {datetime.date.today()}"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg.set_content("Hi, Innaiku update panna files mattum ZIP panni anupapatuள்ளது.")

            with open(actual_zip_file, 'rb') as f:
                file_data = f.read()
            msg.add_attachment(file_data, maintype='application', subtype='zip', filename=f"updates_{datetime.date.today()}.zip")

            try:
                print("Connecting to Gmail Server...")
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    print("Login Successful! Sending ZIP...")
                    server.send_message(msg)
                    print(f"🎉 Success! Today's ZIP sent successfully to {receiver_email}!")
            except Exception as e:
                print(f"❌ SMTP Error: {e}")

            shutil.rmtree(temp_sync_folder)
            if os.path.exists(actual_zip_file):
                os.remove(actual_zip_file)
                print("🧹 Cleaned temporary workspace files.")

        time.sleep(60)  
        print(f"\n⏰ Waiting for tomorrow's schedule...")

    time.sleep(30)
