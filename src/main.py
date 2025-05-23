import argparse
from datetime import datetime # This imports the datetime class from the module
from pathlib import Path
from webScraping import *
from logger import *

outdir = Path.cwd() / "downloads"

def main():
    parser = argparse.ArgumentParser(description="SGX Derivatives File Downloader")
    parser.add_argument('--today', action='store_true',help='Download today\'s files')
    parser.add_argument('--on_date', help='Download for a single date (DD-MM-YYYY)')
    parser.add_argument('--start_date', help='Start date for a range (DD-MM-YYYY)')
    parser.add_argument('--end_date', help='End date for a range (DD-MM-YYYY)')
    parser.add_argument('--retry_failed',action='store_true', help='Retry downloading failed dates')

    args = parser.parse_args()
    
    if args.today:
        download_file(datetime.now(), outdir)
    elif args.on_date:
        date = datetime.strptime(args.on_date, '%d-%m-%Y')
        download_file(date, outdir)
    elif args.start_date and args.end_date:
        start_date = datetime.strptime(args.start_date, '%d-%m-%Y')
        end_date = datetime.strptime(args.end_date, '%d-%m-%Y')
        download_multiple_files(start_date, end_date, outdir)
    elif args.retry_failed:
        retry_failed_downloads(outdir)
    else:
        print("Error: Missing required arguments. Use --help for usage information.")

if __name__ == '__main__':
    main()