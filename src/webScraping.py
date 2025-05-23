import fnmatch
from datetime import datetime
from pathlib import Path
import requests
from logger import *
from utils.date_convert import *
from utils.csvFile import *

url = "https://links.sgx.com/1.0.0/derivatives-historical/{index}/{file}"

    
def is_error_response(
        content: bytes) -> bool:
 
    text = content.decode('utf-8', errors='ignore')

    if "<html" in text.lower() and "no record found" in text.lower():
        return True
    return False

def convert_url(file ,index):
     if fnmatch.fnmatch(file, "TC_*.txt"): 
        file_url = url.format(index=index, file="TC.txt")
        return file_url
     else:
        file_url = url.format(index=index, file=file)
        return file_url


def process_file(
    file : str,
    date_str : str,
    index : int,
    outdir : str,
) -> bool:
    try:
        file_url = convert_url(file,index)
        outdir = outdir / file
        success = True

        if outdir.exists():
            downloadLog.info(f"File already exists, skipping: {file} - {date_str} - {index}")
            return True

        try:
            response = requests.get(file_url, stream=True)
            response.raise_for_status()

            if "text/html" in response.headers.get("Content-Type", "") or is_error_response(response.content):
                success = False
                create_fail_csv(date_str,file,"Not Found",index)
                errMsg = f"No content - {file} - {date_str} - {index}"
                errorLog().error(errMsg)
                return success

            with open(outdir, "wb") as f:
                f.write(response.content)

            downloadLog.info(f"Downloaded successfully: {file} - {date_str} - {index}")

            return success
        except requests.RequestException as e:
            errMsg = f"Request failed for {file_url}: {e}"
            errorLog.error(errMsg)
            return False
        except Exception as e:
            errMsg = f"Unexpected error writing file {file}: {e}"
            errorLog.error(errMsg)
            return False
        
        return True
    except Exception as e:
        errMsg = f"Error processing file: {e}"
        errorLog.error(errMsg)
        return False



def download_file(
    dates: datetime,
    outdir: Path
) -> bool:

    try:
        success = True
        index = date_to_index(dates)
        date_str = dates.strftime('%Y%m%d')
        outdir = outdir / f"SGX_{date_str}"
        outdir.mkdir(parents=True, exist_ok=True)

        files = [
            f"WEBPXTICK_DT-{date_str}.zip",
            "TickData_structure.dat",
            f"TC_{date_str}.txt",
            "TC_structure.dat"
        ]

        infoLog.info(f"Downloading files for date: {date_str}, index: {index}")
        
        for file in files:
            try:
                success = process_file(file, date_str, index, outdir)
                
            except Exception as e:
                errMsg = f"Error processing file {file}: {e}"
                errorLog.error(errMsg)
                success = False
        return success
    except (ValueError , TypeError) as e:
        errMsg = f"Invalid date format: {e}"
        errorLog.error(errMsg)
        return False
    
def download_multiple_files(
        start_date: datetime,
        end_date :datetime,
        outdir: Path
) -> bool:

    try:
        if start_date > end_date:
            errMsg ="Start date cannot be after end date."
            errorLog.error(errMsg)
            raise ValueError(errMsg)
        
        index_list = date_to_index_in_multiple_file(start_date,end_date)
        date_list = get_date_list(start_date,end_date)

        infoLog.info(f"Downloading files from {start_date.strftime('%Y%m%d')} to {end_date.strftime('%Y%m%d')}")

        success = True
        for i, date_str in enumerate(date_list):
            dir_path = outdir / f"SGX_{date_str}"
            dir_path.mkdir(parents=True, exist_ok=True)
            current_index = index_list[i]

            files = [
                f"WEBPXTICK_DT-{date_str}.zip",
                f"TC_{date_str}.txt",
                "TickData_structure.dat",
                "TC_structure.dat"
            ]

            for file in files:
                if not process_file(file, date_str, current_index, dir_path):
                    success = False

        return success

    except (TypeError, ValueError) as e:
        errMsg = f"Invalid date format: {e}"
        errorLog.error(errMsg)
        return False
    
def retry_failed_downloads(outdir: Path) -> bool:
    try:
        success = True
        df = read_csv()

        if df is None or df.empty:
            infoLog.info("No failed downloads to retry.")
            return False

        successful_indices = []

        for i, row in df.iterrows():
            date_str = row['date_str']
            file_name = row['error_fileName']
            retry_count = int(row.get('retry_count', 0))
            index_val = row['index']
            dir_path = outdir / f"SGX_{date_str}"
            dir_path.mkdir(parents=True, exist_ok=True)

            infoLog.info(f"Retrying failed file: {file_name} | Date: {date_str} | Index: {index_val} | Attempt: {retry_count + 1}")

            # Retry the file
            if process_file(file_name, date_str, index_val, dir_path):
                successful_indices.append(i)
            else:
                success = False
                df.at[i, 'retry_count'] = retry_count + 1  

        if successful_indices:
            df.drop(index=successful_indices, inplace=True)
            infoLog.info(f"Removed {len(successful_indices)} successfully retried files from retry log.")

        df.to_csv("logs/downloads_failed.csv", index=False)
        infoLog.info("Retry log updated.")

        return success
    except (TypeError, ValueError) as e:
        errMsg = f"Retry download files failed: {e}"
        errorLog.error(errMsg)
        raise
