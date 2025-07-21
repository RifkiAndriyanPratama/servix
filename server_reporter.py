import psutil
import os
from datetime import datetime

LOG_FILE = "/home/yui/Documents/servix/server.log"
REPORT_DIR = "/home/yui/Documents/servix/reports"

metrics_data = [] #menyimpan list

# Ambil tangal hari ini
today = datetime.today().strftime('%Y-%m-%d')
REPORT_FILE = f"{REPORT_DIR}/daily_report_{today}.txt"

# Memastikan foldernya ada
os.makedirs(REPORT_DIR, exist_ok=True)

with open(LOG_FILE, "r") as f:
    for line in f:
        cleaned_line = line.strip()
        if not cleaned_line:
            continue

        parts = cleaned_line.split(",")
        current_metric = {}
        current_metric['timestamp'] = parts[0]

        # loop bagian setelah timestamp
        for i in range(1, len(parts)):
            key_value_pair = parts[i]
            key_val_split = key_value_pair.split('=')

            if len(key_val_split) == 2:
                key = key_val_split[0].strip()
                value_str = key_val_split[1].strip()

                try:
                    current_metric[key] = float(value_str)
                except ValueError:
                    current_metric[key] = value_str
            else:
                print(f"Warning: Skipping malformed part in line: {key_value_pair}")
        metrics_data.append(current_metric)

# Mulai menganalisis data
if not metrics_data: #cek jika log kosong
    print("No data loaded from log file, Cannot generate report.")
else:
    # inisialisasi variabel buat penghitungan
    total_cpu = 0
    max_cpu = 0
    total_ram = 0
    max_ram = 0
    total_disk = 0
    max_disk = 0

    cpu_alerts = 0
    ram_alerts = 0
    disk_alerts = 0
    cpu_warnings = 0
    ram_warnings = 0
    disk_warnings = 0

    # loop melalui setiap data entry yang sudah diparsing
    for entry in metrics_data:
        if 'CPU' in entry and isinstance(entry['CPU'], (int, float)):
            total_cpu += entry['CPU']
            if entry['CPU'] > max_cpu:
                max_cpu = entry['CPU']

        if 'RAM' in entry and isinstance(entry['RAM'], (int, float)):
            total_ram += entry['RAM']
            if entry['RAM'] > max_ram:
                max_ram = entry['RAM']

        if 'DISK' in entry and isinstance(entry['DISK'], (int, float)):
            total_disk += entry['DISK']
            if entry['DISK'] > max_disk:
                max_disk = entry['DISK']
        
        # Menghitung jumlah alert dan warning
        if 'CPU_STATUS' in entry:
            if entry['CPU_STATUS'] == 'ALERT':
                cpu_alerts += 1
            elif entry['CPU_STATUS'] == 'WARNING':
                cpu_warnings += 1
        
        if 'RAM_STATUS' in entry:
            if entry['RAM_STATUS'] == 'ALERT':
                ram_alerts += 1
            if entry['RAM_STATUS'] == 'WARNING':
                ram_warnings += 1
        
        if 'DISK_STATUS' in entry:
            if entry['DISK_STATUS'] == 'ALERT':
                disk_alerts += 1
            elif entry['DISK_STATUS'] == 'WARNING':
                disk_warnings += 1

# Menghitung rata-rata
num_entries = len(metrics_data)
avg_cpu = total_cpu / num_entries
avg_ram = total_ram / num_entries
avg_disk = total_disk / num_entries

# Menentukan rentang waktu laporan
first_timestamp_str = metrics_data[0]['timestamp']
last_timestamp_str = metrics_data[-1]['timestamp']

# Tulis laporan 
with open(REPORT_FILE, 'w') as f:
    f.write("\n--- Server Health Report ---\n")
    f.write(f"Report Period     : {first_timestamp_str} to {last_timestamp_str}\n")
    f.write(f"Total Data Points : {num_entries}\n")

    f.write("\n--- Usage Statistics ---\n")
    f.write(f"Average CPU Usage : {avg_cpu:.2f}%\n")
    f.write(f"Peak CPU Usage    : {max_cpu:.2f}%\n")
    f.write(f"Average RAM Usage : {avg_ram:.2f}%\n")
    f.write(f"Peak RAM Usage    : {max_ram:.2f}%\n")
    f.write(f"Average Disk Usage: {avg_disk:.2f}%\n")
    f.write(f"Peak Disk Usage   : {max_disk:.2f}%\n")

    f.write("\n--- Alerts & Warnings ---\n")
    f.write(f"CPU Alerts        : {cpu_alerts}\n")
    f.write(f"CPU Warnings      : {cpu_warnings}\n")
    f.write(f"RAM Alerts        : {ram_alerts}\n")
    f.write(f"RAM Warnings      : {ram_warnings}\n")
    f.write(f"Disk Alerts       : {disk_alerts}\n")
    f.write(f"Disk Warnings     : {disk_warnings}\n")
