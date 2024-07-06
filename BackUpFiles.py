import shutil
import time
from datetime import datetime
import os

def backup_file(src_file, backup_directory):
    # Ensure backup directory exists
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)

    # Create a backup file path with a timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    backup_path = os.path.join(backup_directory, f'backup_{timestamp}_{os.path.basename(src_file)}')

    try:
        shutil.copy2(src_file, backup_path)
        print(f'Backup created at {backup_path}')
    except Exception as e:
        print(f'Error creating backup: {e}')

# Example usage
src_file = 'SuperSecretFile.txt'  # Replace with the path to your file
backup_directory = 'backups'

while True:
    backup_file(src_file, backup_directory)
    time.sleep(3600)  # Backup every hour
