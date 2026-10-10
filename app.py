from flask import Flask, render_template, request, send_file
import hashlib
import os
import json
import requests
from datetime import datetime
from reportlab.pdfgen import canvas
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)

# =========================================
# CONFIG
# =========================================

UPLOAD_FOLDER = "uploads"
HASH_DB = "hashes.json"
HISTORY_DB = "scan_history.json"

# VIRUSTOTAL API KEY

API_KEY = "YOUR_VIRUSTOTAL_API_KEY"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# =========================================
# CREATE UPLOAD FOLDER
# =========================================

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================================
# GENERATE SHA256 HASH
# =========================================

def generate_hash(filepath):

    sha256 = hashlib.sha256()

    with open(filepath, "rb") as f:

        while chunk := f.read(4096):

            sha256.update(chunk)

    return sha256.hexdigest()

# =========================================
# LOAD HASH DATABASE
# =========================================

def load_hashes():

    if os.path.exists(HASH_DB):

        try:

            with open(HASH_DB, "r") as f:

                return json.load(f)

        except:

            return {}

    return {}

# =========================================
# SAVE HASH DATABASE
# =========================================

def save_hashes(data):

    with open(HASH_DB, "w") as f:

        json.dump(data, f, indent=4)

# =========================================
# LOAD HISTORY
# =========================================

def load_history():

    if os.path.exists(HISTORY_DB):

        try:

            with open(HISTORY_DB, "r") as f:

                return json.load(f)

        except:

            return []

    return []

# =========================================
# SAVE HISTORY
# =========================================

def save_history(data):

    with open(HISTORY_DB, "w") as f:

        json.dump(data, f, indent=4)

# =========================================
# VIRUSTOTAL API
# =========================================

def check_virustotal(file_hash):

    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"

    headers = {

        "x-apikey": API_KEY

    }

    try:

        response = requests.get(
            url,
            headers=headers
        )

        if response.status_code == 200:

            data = response.json()

            malicious = data["data"]["attributes"][
                "last_analysis_stats"
            ]["malicious"]

            return malicious

    except:

        return 0

    return 0

# =========================================
# LIVE FOLDER MONITOR
# =========================================

class MonitorHandler(FileSystemEventHandler):

    def on_created(self, event):

        print(f"NEW FILE DETECTED: {event.src_path}")

    def on_modified(self, event):

        print(f"FILE MODIFIED: {event.src_path}")

    def on_deleted(self, event):

        print(f"FILE DELETED: {event.src_path}")

# =========================================
# HOME PAGE
# =========================================

@app.route("/", methods=["GET", "POST"])

def index():

    hash_result = None
    filename = None
    status = None
    threat_score = 0
    scan_time = None
    file_size = None
    file_type = None

    SCAN_HISTORY = load_history()

    if request.method == "POST":

        # =========================================
        # URL SCAN
        # =========================================

        url = request.form.get("url")

        if url and url.strip() != "":

            filename = url

            suspicious_words = [

                "hack",
                "crack",
                "free",
                "gift",
                "bonus",
                "casino",
                "bitcoin",
                "login",
                "verify",
                "bank"

            ]

            if url.startswith("https://"):

                if any(word in url.lower()
                       for word in suspicious_words):

                    status = "SUSPICIOUS URL"
                    threat_score = 75

                else:

                    status = "SAFE URL"
                    threat_score = 5

            else:

                status = "WARNING - INVALID URL"
                threat_score = 90

            hash_result = "URL Scan Completed"

            scan_time = datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

            file_type = "URL"
            file_size = 0

            SCAN_HISTORY.append({

                "file": filename,

                "status": status

            })

            save_history(SCAN_HISTORY)

        # =========================================
        # FILE SCAN
        # =========================================

        file = request.files.get("file")

        if file and file.filename != "":

            filepath = os.path.join(
                UPLOAD_FOLDER,
                file.filename
            )

            file.save(filepath)

            filename = file.filename

            file_size = round(
                os.path.getsize(filepath) / 1024,
                2
            )

            if "." in filename:

                file_type = filename.split(".")[-1].upper()

            else:

                file_type = "UNKNOWN"

            scan_time = datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

            # =========================================
            # MALWARE DETECTION
            # =========================================

            dangerous_extensions = [

                ".exe",
                ".bat",
                ".vbs",
                ".scr",
                ".ps1"

            ]

            malware_words = [

                "hack",
                "crack",
                "virus",
                "trojan",
                "payload",
                "keylogger"

            ]

            file_ext = os.path.splitext(filename)[1]

            if file_ext.lower() in dangerous_extensions:

                status = "WARNING - POSSIBLE MALWARE"

                threat_score = 85

            elif any(word in filename.lower()
                     for word in malware_words):

                status = "SUSPICIOUS FILE"

                threat_score = 75

            # =========================================
            # HASH GENERATION
            # =========================================

            current_hash = generate_hash(filepath)

            hashes = load_hashes()

            # =========================================
            # VIRUSTOTAL CHECK
            # =========================================

            vt_result = check_virustotal(current_hash)

            if vt_result > 0:

                status = "MALWARE DETECTED"

                threat_score = 95

            # =========================================
            # FILE INTEGRITY CHECK
            # =========================================

            if filename not in hashes:

                hashes[filename] = current_hash

                save_hashes(hashes)

                if status is None:

                    status = "SAFE - HASH SAVED"

                    threat_score = 5

            else:

                saved_hash = hashes[filename]

                if saved_hash == current_hash:

                    if status is None:

                        status = "SAFE - INTEGRITY OK"

                        threat_score = 5

                else:

                    status = "WARNING - FILE TAMPERED"

                    threat_score = 90

            hash_result = current_hash

            SCAN_HISTORY.append({

                "file": filename,

                "status": status

            })

            save_history(SCAN_HISTORY)

    # =========================================
    # DASHBOARD COUNTS
    # =========================================

    files_scanned = len(SCAN_HISTORY)

    safe_count = sum(

        1 for item in SCAN_HISTORY

        if "SAFE" in item["status"]

    )

    tampered_count = sum(

        1 for item in SCAN_HISTORY

        if "TAMPERED" in item["status"]

    )

    warning_count = sum(

        1 for item in SCAN_HISTORY

        if "WARNING" in item["status"]

    )

    # =========================================
    # RENDER TEMPLATE
    # =========================================

    return render_template(

        "index.html",

        hash_result=hash_result,

        filename=filename,

        status=status,

        threat_score=threat_score,

        history=SCAN_HISTORY,

        files_scanned=files_scanned,

        safe_count=safe_count,

        tampered_count=tampered_count,

        warning_count=warning_count,

        scan_time=scan_time,

        file_size=file_size,

        file_type=file_type
    )

# =========================================
# FOLDER MONITOR
# =========================================

@app.route("/folder-monitor")

def folder_monitor():

    monitored_folder = UPLOAD_FOLDER

    folder_files = []

    dangerous_extensions = [

        ".exe",
        ".bat",
        ".vbs",
        ".scr",
        ".ps1"

    ]

    malware_words = [

        "hack",
        "crack",
        "virus",
        "trojan",
        "payload",
        "keylogger"

    ]

    for file in os.listdir(monitored_folder):

        filepath = os.path.join(
            monitored_folder,
            file
        )

        if os.path.isfile(filepath):

            file_hash = generate_hash(filepath)

            file_ext = os.path.splitext(file)[1]

            status = "SAFE FILE"
            threat_score = 5

            if file_ext.lower() in dangerous_extensions:

                status = "WARNING - POSSIBLE MALWARE"
                threat_score = 85

            elif any(word in file.lower()
                     for word in malware_words):

                status = "SUSPICIOUS FILE"
                threat_score = 75

            folder_files.append({

                "name": file,

                "hash": file_hash,

                "status": status,

                "threat_score": threat_score

            })

    return render_template(

        "folder.html",

        files=folder_files
    )

# =========================================
# PDF REPORT
# =========================================

@app.route("/download-report")

def download_report():

    report_path = "scan_report.pdf"

    c = canvas.Canvas(report_path)

    c.setFont("Helvetica-Bold", 18)

    c.drawString(

        170,
        800,
        "MANI SECURE REPORT"

    )

    history = load_history()

    y = 760

    for item in history:

        c.setFont("Helvetica", 12)

        c.drawString(

            50,
            y,
            f"{item['file']} - {item['status']}"

        )

        y -= 25

    c.save()

    return send_file(

        report_path,

        as_attachment=True
    )

# =========================================
# RUN SERVER
# =========================================

if __name__ == "__main__":

    event_handler = MonitorHandler()

    observer = Observer()

    observer.schedule(

        event_handler,

        path=UPLOAD_FOLDER,

        recursive=True
    )

    observer.start()

    app.run(debug=True)