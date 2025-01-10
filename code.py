import os
import sys
import shutil
import datetime
import argparse
import subprocess

# Constants
KEEP_DAYS_DEFAULT = 5

def usage():
    print("""
Vol remove arbitrage process to pre-sync previous business day's EOD dump file.
Usage: script.py -i <vox report file directory> 
       [-k <number of business days> Keeps stale files. Default is 5]
""")
    sys.exit(-1)

def print_log(log_message):
    dt = datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
    print(f"{dt} - {log_message}")

def sync_and_clean_vox_eod_dump_file(from_date, to_date, input_file_dir, keep_days):
    from_year, from_month, from_day = from_date[:4], from_date[4:6], from_date[6:8]
    to_year, to_month, to_day = to_date[:4], to_date[4:6], to_date[6:8]

    from_dir = os.path.join(input_file_dir, from_year, from_month, from_day)
    clean_cmd = f"find {from_dir} -mtime +{keep_days} -exec rm -f {{}} \\;"
    print_log(f"Executing clean command: {clean_cmd}")
    subprocess.run(clean_cmd, shell=True)

    to_dir = os.path.join(input_file_dir, to_year, to_month, to_day)
    mkdir_cmd = f"mkdir -p {to_dir}"
    print_log(f"Executing mkdir command: {mkdir_cmd}")
    subprocess.run(mkdir_cmd, shell=True)

    rsync_cmd = f"rsync -trp {from_dir}/ {to_dir}/"
    print_log(f"Executing rsync command: {rsync_cmd}")
    result = subprocess.run(rsync_cmd, shell=True, capture_output=True, text=True)
    print_log(result.stdout)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True, help="vox report file directory")
    parser.add_argument("-k", type=int, default=KEEP_DAYS_DEFAULT, help="Number of business days to keep stale files")

    args = parser.parse_args()

    input_file_dir = args.i
    keep_days = args.k

    if not os.path.exists(input_file_dir):
        usage()

    today = datetime.datetime.now().strftime("%Y%m%d")
    print_log(f"Today is {today}. Sync EOD dump from previous dates.")

    previous_working_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    sync_and_clean_vox_eod_dump_file(previous_working_date, today, input_file_dir, keep_days)

if __name__ == "__main__":
    main()
