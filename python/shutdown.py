import os
import time
from datetime import datetime

shutdown_time = "14:10"  # 11:00 PM

while True:
    now = datetime.now().strftime("%H:%M")

    if now == shutdown_time:
        os.system("shutdown /s /f /t 0")
        break

    time.sleep(30)
