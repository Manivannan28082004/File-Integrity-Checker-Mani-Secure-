# 🛡️ Mani Secure — File Integrity Checker

**A Python-Based Cybersecurity Tool for File Integrity Monitoring**

Monitor file integrity, detect unexpected file modifications, and help protect important files using cryptographic hashing techniques such as SHA-256.

## 📌 Project Overview

Mani Secure is a cybersecurity project designed to check whether files have been modified by comparing their cryptographic hash values. It helps users identify unexpected changes to files and supports basic file integrity monitoring.

## ✨ Key Features

- **File Integrity Verification:** Check file integrity using cryptographic hashes.
- **SHA-256 Hashing:** Generate hash values to identify changes in file contents.
- **File Change Detection:** Compare file hashes to identify modifications.
- **Scan History:** Maintain scan-related records using JSON files.
- **Report Generation:** Includes a PDF report file in the project.
- **Web Interface:** Uses HTML templates and CSS for the user interface.

*Note: Features listed above should match the functionality implemented in your code.*

## ⚙️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic |
| SHA-256 | Cryptographic file hashing |
| HTML | Web page structure |
| CSS | User interface styling |
| JSON | Store hash data and scan history |
| Flask | Web framework, if used by the application |

## 🔄 How It Works

1. Select or provide a file for integrity checking.
2. Generate its cryptographic hash using SHA-256.
3. Compare the current hash with the previously stored hash, when available.
4. Identify whether the file content has changed.
5. Review the scan results and available reports.

## 🚀 Installation and Setup

### Prerequisites

- Python 3.x
- Visual Studio Code
- Required Python packages

### Run the Project

1. Clone this repository:

   ```bash
   git clone https://github.com/Manivannan28082004/File-Integrity-Checker-Mani-Secure-.git
   ```

2. Navigate to the project folder:

   ```bash
   cd File-Integrity-Checker-Mani-Secure-
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Install the dependencies listed in `requirements.txt`, if available:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the application using the entry point configured in your project. If `app.py` contains the Flask application entry point, use:

   ```bash
   python app.py
   ```

6. Open the local URL displayed in the terminal.

## 📁 Project Structure

```text
Mani-Secure/
├── app.py
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   └── folder.html
├── hashes.json
├── scan_history.json
├── scan_report.pdf
└── README.md
```

*This is an example structure. Update it to match the actual files in your repository.*

## 🔐 Security Benefits

- Helps identify unexpected changes to monitored files.
- Supports integrity verification using cryptographic hashes.
- Provides a foundation for file integrity monitoring and security auditing.

**Important:** Hash comparison can detect changes, but it does not by itself prevent file modifications or guarantee that a file is safe.

## 🔮 Future Enhancements

- Real-time file monitoring
- Email alerts for detected changes
- Improved scan history and reporting
- User authentication and access control

## 👨‍💻 Author

**Manivannan K**

Cybersecurity | Ethical Hacking | Security Monitoring

GitHub: [Manivannan28082004](https://github.com/Manivannan28082004)

---

⭐ If you find this project useful, consider starring the repository.
