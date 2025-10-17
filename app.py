import os, uuid
from io import BytesIO
from flask import Flask, request, render_template, redirect, url_for, send_file, flash
from dotenv import load_dotenv
import sqlite3
from datetime import datetime
from crypto_utils import ensure_key_from_base64, encrypt_bytes, decrypt_bytes, pack_to_store, unpack_from_store, sha256_bytes

load_dotenv()

MASTER_KEY = ensure_key_from_base64(os.getenv("MASTER_KEY"))
ENCRYPTED_FOLDER = os.getenv("ENCRYPTED_FOLDER", "./encrypted")
DB_PATH = os.getenv("DATABASE", "./files.db")
MAX_CONTENT = int(os.getenv("MAX_CONTENT_LENGTH", 50*1024*1024))

os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "devsecret")
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT

# Database setup
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        orig_name TEXT NOT NULL,
        stored_name TEXT NOT NULL UNIQUE,
        sha256 TEXT NOT NULL,
        size INTEGER NOT NULL,
        uploaded_at TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

init_db()

def insert_file(orig_name, stored_name, sha, size):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO files (orig_name, stored_name, sha256, size, uploaded_at) VALUES (?, ?, ?, ?, ?)',
              (orig_name, stored_name, sha, size, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def list_files():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, orig_name, stored_name, sha256, size, uploaded_at FROM files ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def get_file_by_storedname(stored_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, orig_name, stored_name, sha256, size, uploaded_at FROM files WHERE stored_name=?', (stored_name,))
    row = c.fetchone()
    conn.close()
    return row

@app.route('/')
def index():
    return render_template('list.html', files=list_files())

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    f = request.files.get('file')
    if not f:
        flash('No file selected')
        return redirect(url_for('upload'))
    data = f.read()
    sha = sha256_bytes(data)
    enc = encrypt_bytes(data, MASTER_KEY)
    stored_name = str(uuid.uuid4()) + '.enc'
    path = os.path.join(ENCRYPTED_FOLDER, stored_name)
    with open(path, 'wb') as fh:
        fh.write(pack_to_store(enc['ciphertext'], enc['nonce'], enc['tag']))
    insert_file(f.filename, stored_name, sha, len(data))
    flash('File uploaded and encrypted successfully')
    return redirect(url_for('index'))

@app.route('/download/<stored_name>')
def download(stored_name):
    rec = get_file_by_storedname(stored_name)
    if not rec:
        flash('File not found')
        return redirect(url_for('index'))
    path = os.path.join(ENCRYPTED_FOLDER, stored_name)
    if not os.path.exists(path):
        flash('Encrypted file missing')
        return redirect(url_for('index'))
    try:
        with open(path,'rb') as fh:
            stored = fh.read()
        ciphertext, nonce, tag = unpack_from_store(stored)
        plaintext = decrypt_bytes(ciphertext, nonce, tag, MASTER_KEY)
    except Exception:
        flash('Decryption failed (tampered file or wrong key)')
        return redirect(url_for('index'))
    return send_file(BytesIO(plaintext), as_attachment=True, download_name=rec[1])

if __name__ == '__main__':
    app.run(debug=True)
