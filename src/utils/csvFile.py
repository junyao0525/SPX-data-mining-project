import csv
import os
from pathlib import Path
import pandas as pd
from logger import *

def setup_failed_download_tracker():

    Path("logs").mkdir(parents=True, exist_ok=True)

    csv_file = "logs/downloads_failed.csv"

    fields = ['date_str','index', 'error_fileName', 'error_message', 'retry_count']

    if not os.path.exists(csv_file):
        with open(csv_file, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
    
    return csv_file

def create_fail_csv(
    date_str: str,
    file_name: str,
    error_message: str,
    index: int,
    retry_count: int = 0):
    
    try:
        csv_file = "logs/downloads_failed.csv"
    
        # Create logs directory if it doesn't exist
        Path("logs").mkdir(parents=True, exist_ok=True)
        
        # Check if CSV file exists and create it if it doesn't
        if not os.path.exists(csv_file):
            setup_failed_download_tracker()
        
        # Check if file exists and has content
        exists = os.path.isfile(csv_file) and os.path.getsize(csv_file) > 0
        
        if exists:
            try:
                df = pd.read_csv(csv_file)
                infoLog.info(f"CSV file exists with {len(df)} entries")
            
                if 'index' in df.columns and 'error_fileName' in df.columns:
                    matching_entries = df[(df['index'] == index) & (df['error_fileName'] == file_name)]
                    # downloadLog.info(f"Found {len(matching_entries)} matching entries for index {index}, file {file_name}")
                    if not matching_entries.empty:
                        row_index = matching_entries.index[0]
                        df.at[row_index, 'retry_count'] = df.at[row_index, 'retry_count'] + 1
                        df.at[row_index, 'error_message'] = error_message
                        
                        df.to_csv(csv_file, index=False)
                        infoLog.info(f"Updated retry count for index {index}, file {file_name}")
                        return
                
                new_row = pd.DataFrame({
                    'date_str': [date_str],
                    'index': [index],
                    'error_fileName': [file_name],
                    'error_message': [error_message],
                    'retry_count': [retry_count]
                })
                
                df = pd.concat([df, new_row])
                df.to_csv(csv_file, index=False)
                infoLog.info(f"Added new entry for index {index}, file {file_name}")
                
            except Exception as e:
                errorLog.error(f"Error processing CSV: {e}")
        else:
            with open(csv_file, "a", newline='') as f:
                writer = csv.writer(f)
                if not exists:
                    writer.writerow(['date_str','index', 'error_fileName', 'error_message', 'retry_count'])
                writer.writerow([
                    date_str,
                    index,
                    file_name,
                    error_message,
                    retry_count
                ])
            infoLog.info(f"Created new file and added entry for index {index}, file {file_name}")
            
    except Exception as e:
        errorLog.error(f"Error in create_fail_csv: {e}")

def read_csv():
    csv_file = "logs/downloads_failed.csv"
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        infoLog.info(f"CSV file exists with {len(df)} entries")
        return df
    else:
        infoLog.error("CSV file does not exist")
        return None