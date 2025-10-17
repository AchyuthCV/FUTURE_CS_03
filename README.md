# Secure File Sharing System with AES Encryption - Future Interns Task 3

🔐 **Secure File Sharing System** is a web application that allows users to safely upload and download files. Security is the main focus — all files are encrypted using **AES (Advanced Encryption Standard)** before storage and decrypted during download.

This project simulates real-world secure data sharing environments, such as healthcare, legal, or corporate systems.

---

## 🎯 Objectives

- Develop a web portal using **Python Flask** for file uploads and downloads.
- Implement **AES encryption** to protect files at rest.
- Provide a simple and user-friendly interface for uploading and retrieving files.
- Ensure basic encryption key management and security best practices.
- Document the system architecture and security measures.

---

## ✅ Key Features

- Secure file upload and download
- AES encryption for all files
- Basic encryption key handling
- User-friendly interface
- Well-documented code and architecture

---

## 🛠️ Tools & Technologies

- **Python 3.x**
- **Flask** – Backend web framework ([Flask Docs](https://flask.palletsprojects.com/en/latest/))
- **PyCryptodome** – Python cryptography library ([Docs](https://pycryptodome.readthedocs.io/en/latest/))
- **HTML / CSS / JavaScript** – Frontend basics
- **Git & GitHub** – Version control
- **Postman / curl** – API testing (optional)

---

## 🗂️ Repository Structure

FUTURE_CS_03/
├── app.py # Main Flask application
├── crypto_utils.py # AES encryption/decryption functions
├── templates/
│ ├── upload.html # File upload interface
│ └── list.html # File listing & download interface
├── requirements.txt # Python dependencies
├── README.md # Project documentation

## Install dependencies
pip install -r requirements.txt

## Run the application
python app.py

## Access the system
Open your browser and go to http://127.0.0.1:5000/ to upload and download files securely.

## 🔑 Security Overview

Encryption Algorithm: AES (Advanced Encryption Standard)

File Protection: All files are stored encrypted to prevent unauthorized access.

Key Handling: Encryption and decryption keys are managed securely within the application.

Integrity Check: Ensures that uploaded and downloaded files remain unaltered.

 ## 🎓 Skills Gained

Web development using Flask (backend & frontend)

Implementing encryption algorithms (AES)

Secure file handling and data protection

Basic cryptography concepts and key management

Version control using Git & GitHub

## 📄 References

Flask Documentation

PyCryptodome Documentation

MDN Web Docs – HTML/CSS/JS
