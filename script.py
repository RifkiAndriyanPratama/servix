import psutil
import time
from datetime import datetime

LOG_FILE = "server.log"

def collect_and_log():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu_usage = psutil.cpu_percent(interval=1)
    mem_info = psutil.virtual_memory()
    ram_usage = mem_info.percent
    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent

    log = f"{timestamp}, CPU={cpu_usage}, RAM={ram_usage}, DISK={disk_usage}"

    with open(LOG_FILE, 'a') as f:
        f.write(log)
    print(f"Logged at {timestamp}")

# menjalankan looping untuk mengumpulkan data secara berkala
while True:
    collect_and_log()
    time.sleep(300)