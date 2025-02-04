import os
import shutil
import re
from datetime import datetime

def organize_postgres_files(base_dir):
    raw_dir = os.path.join(base_dir, 'raw')
    
    # Ensure the raw directory exists
    if not os.path.exists(raw_dir):
        raise FileNotFoundError(f"The directory {raw_dir} does not exist.")

    print(f"Scanning directory: {raw_dir}")

    # Iterate over all files in the raw directory
    for filename in os.listdir(raw_dir):
        print(f"Found file: {filename}")

        if filename.startswith('raw_public') and filename.endswith('.csv'):
            print(f"Processing file: {filename}")
            
            # Extract table_name and date using regex
            match = re.match(r'raw_public-(\w+)_(\d{4}-\d{2}-\d{2})\.csv', filename)
            if match:
                table_name, date = match.groups()
                print(f"Extracted table_name: {table_name}, date: {date}")
                
                # Create table_name directory if it doesn't exist
                table_dir = os.path.join(raw_dir, table_name)
                if not os.path.exists(table_dir):
                    os.makedirs(table_dir)
                    print(f"Created directory: {table_dir}")

                # Create date directory inside table_name directory if it doesn't exist
                date_dir = os.path.join(table_dir, date)
                if not os.path.exists(date_dir):
                    os.makedirs(date_dir)
                    print(f"Created directory: {date_dir}")
                
                # Move the file to the date directory
                src_path = os.path.join(raw_dir, filename)
                dest_path = os.path.join(date_dir, filename)
                shutil.move(src_path, dest_path)
                print(f"Moved {filename} to {dest_path}")
            else:
                print(f"Filename {filename} does not match the expected pattern.")
        else:
            print(f"Skipping file: {filename}")


def organize_csv_files(base_dir):
    raw_dir = os.path.join(base_dir, 'raw')
    
    # Ensure the raw directory exists
    if not os.path.exists(raw_dir):
        raise FileNotFoundError(f"The directory {raw_dir} does not exist.")

    print(f"Scanning directory: {raw_dir}")

    # Iterate over all files in the raw directory
    for filename in os.listdir(raw_dir):
        print(f"Found file: {filename}")

        if filename.startswith('raw_order_') and filename.endswith('.csv'):
            print(f"Processing file: {filename}")
            
            # Extract table_name and date using regex
            match = re.match(r'raw_(\w+)_(\d{4}-\d{2}-\d{2})\.csv', filename)
            if match:
                table_name, date = match.groups()
                print(f"Extracted table_name: {table_name}, date: {date}")
                
                # Create table_name directory if it doesn't exist
                table_dir = os.path.join(raw_dir, table_name)
                if not os.path.exists(table_dir):
                    os.makedirs(table_dir)
                    print(f"Created directory: {table_dir}")

                # Create date directory inside table_name directory if it doesn't exist
                date_dir = os.path.join(table_dir, date)
                if not os.path.exists(date_dir):
                    os.makedirs(date_dir)
                    print(f"Created directory: {date_dir}")
                
                # Move the file to the date directory
                src_path = os.path.join(raw_dir, filename)
                dest_path = os.path.join(date_dir, filename)
                shutil.move(src_path, dest_path)
                print(f"Moved {filename} to {dest_path}")
            else:
                print(f"Filename {filename} does not match the expected pattern.")
        else:
            print(f"Skipping file: {filename}")


def rdy_data_to_go():
    # Define the date format and directories
    today_str = datetime.now().strftime('%Y-%m-%d')
    source_folder = f"/home/tigureis/DNC_engenharia_de_dados/Indicium_Tech_Code_Challenge/data/uploaded/grouped/{today_str}"
    source_file = f"order_merged_detail_{today_str}.csv"
    
    destination_folder = "/home/tigureis/DNC_engenharia_de_dados/Indicium_Tech_Code_Challenge/data/uploaded/to_go/"
    destination_file = os.path.join(destination_folder, "order_merged_detail.csv")

    # Check if the source folder exists
    if not os.path.exists(source_folder):
        raise FileNotFoundError(f"No folder found for date {today_str}: {source_folder}")
    
    # Full path of the source file
    source_file_path = os.path.join(source_folder, source_file)

    # Check if the source file exists
    if not os.path.isfile(source_file_path):
        raise FileNotFoundError(f"The file {source_file} does not exist in the folder {source_folder}")

    # Copy the file to the destination, replacing if it exists
    shutil.copy2(source_file_path, destination_file)

    # Check if the file was replaced or newly copied
    if os.path.exists(destination_file):
        return f"File was successfully copied and replaced at {destination_file}"
    else:
        return f"File was successfully copied to {destination_file}"
