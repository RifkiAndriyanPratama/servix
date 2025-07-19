import psutil
import time
from datetime import datetime

LOG_FILE = "server.log"

def collect_and_log():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # get data cpu
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_status = "OK"
    if cpu_usage > 80:
        cpu_status = "ALERT"
    elif cpu_usage > 60:
        cpu_status = "WARNING"
    
    # get data ram
    mem_info = psutil.virtual_memory()
    ram_usage = mem_info.percent
    ram_status = "OK"
    if ram_usage > 80:
        ram_status = "ALERT"
    elif ram_usage > 60:
        ram_status = "WARNING"

    # get data disk
    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent
    disk_status = "OK"
    if disk_usage > 80:
        disk_status = "ALERT"
    elif disk_usage > 60:
        disk_status = "WARNING"

    log = f"{timestamp}, CPU={cpu_usage}, CPU STATUS={cpu_status} ,RAM={ram_usage}, RAM STATUS={ram_status}, DISK={disk_usage}, DISK STATUS={disk_status}"

    with open(LOG_FILE, "a") as f:
        f.write(log + "\n")
    print(f"Logged at {timestamp}")

# menjalankan looping untuk mengumpulkan data secara berkala
while True:
    collect_and_log()
    time.sleep(3)