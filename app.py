from flask import Flask, request, render_template, send_file
from Crypto.Cipher import AES
import base64
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = b'Sixteen byte key'  # Ensure this key is securely managed

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

class Ransomware:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        padding_length = AES.block_size - len(s) % AES.block_size
        padding = chr(padding_length) * padding_length
        return s + padding

    def encrypt_file(self, file_path):
        with open(file_path, 'rb') as file:
            raw = file.read()

        raw_padded = self.pad(raw.decode('utf-8')).encode('utf-8')
        iv = os.urandom(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted = base64.b64encode(iv + cipher.encrypt(raw_padded))

        encrypted_file_path = file_path + ".enc"
        with open(encrypted_file_path, 'wb') as file:
            file.write(encrypted)

        return encrypted_file_path

class Decryption:
    def __init__(self, key):
        self.key = key

    def unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

    def decrypt_file(self, file_path):
        with open(file_path, 'rb') as file:
            encrypted = file.read()

        encrypted = base64.b64decode(encrypted)
        iv = encrypted[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = self.unpad(cipher.decrypt(encrypted[AES.block_size:])).decode('utf-8')

        decrypted_file_path = file_path.replace(".enc", "")
        with open(decrypted_file_path, 'w') as file:
            file.write(decrypted)

        return decrypted_file_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        ransomware = Ransomware(app.config['SECRET_KEY'])
        encrypted_file_path = ransomware.encrypt_file(file_path)

        return send_file(encrypted_file_path, as_attachment=True)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        decryption = Decryption(app.config['SECRET_KEY'])
        decrypted_file_path = decryption.decrypt_file(file_path)

        return send_file(decrypted_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
