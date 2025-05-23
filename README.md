# SGX Derivatives File Downloader

This project automates the downloading of SGX derivatives files from a specified data source. It supports downloading for a specific date, today's date, a range of dates, or retrying previously failed downloads.

---

## 📆 Project Structure

```
project-root/
│
├── src/
│   ├── main.py                  # Entry point for execution
│   ├── webScraping.py           # File for web scraping
│   ├── logger.py                # Setup logger
│   └── utils/                   # Logging, URL conversion, etc.
│       ├── csvFile/             # CRUD operations
│       └── date_convert/        # Convert the date into index
│
├── logs/                        # Logs for success and failure
│   ├── downloads_failed.csv     # Save Failed downloads
│   ├── info.log                 # Logs for info messages
│   ├── download.log             # Logs for successful downloads
│   └── error.log                # Logs for errors
│
├── donwloads/                  # Store downloaded files
├── requirements.txt            # Python package dependencies
└── README.md                   # Project documentation
```

---

## 🚀 Getting Started

### 🔧 Prerequisites

In this project are using python 3.11.11

```bash
pip install -r requirements.txt
```

---

## 📌 Usage

Run the script from the project root:

### ✅ Use today’s date:

```bash
python src/main.py --today
```

### ✅ Use a specific date:

```bash
python src/main.py --on_date 2022-01-01
```

### ✅ Use a range of dates:

```bash
python src/main.py --from_date 2022-01-01 --to_date 2022-01-02
```

### ✅ Retry failed downloads:

```bash
python src/main.py --retry_failed
```

---

## 🧩 Functional Features

* ✅ Download SGX derivatives data for one or more dates.
* 🔁 Retry mechanism for previously failed downloads.
* 📁 File existence check to avoid redundant downloads.
* 📄 Failures are logged in CSV files under name `downloads_failed.csv`.
* 📊 Logging with timestamps and download status in `/logs`.

---

## 📝 Notes

* The retry logic currently has **no limit on retries**, but logs will show how many times a file has been attempted.
* Logs are written using `errorLog()` and `downloadLog` utilities.
* If a file already exists, it is skipped by default.

---

## 🔍 Logging

Log files are generated under the `/logs` directory:

* `download.log`: Tracks successful downloads.
* `error.log`: Captures errors and exceptions.
* `downloads_failed.csv`: Detailed tracking of failed attempts.

---

