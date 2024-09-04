from flask import Flask, render_template, request, send_file
from cryptography.fernet import Fernet
import os
import io
import zipfile
app = Flask(__name__)

# Generate and store a key for encryption/decryption
key = Fernet.generate_key()
cipher = Fernet(key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_files():
    files = request.files.getlist('files')
    encrypted_files = []

    for file in files:
        filename = file.filename
        file_path = os.path.join('uploads', filename)

        # Save the original file
        file.save(file_path)

        # Read the file data
        with open(file_path, 'rb') as f:
            data = f.read()

        # Encrypt the data
        encrypted_data = cipher.encrypt(data)

        # Save the encrypted file
        encrypted_file_path = os.path.join('encrypted', 'encrypted_' + filename)
        with open(encrypted_file_path, 'wb') as f:
            f.write(encrypted_data)

        encrypted_files.append(encrypted_file_path)

    # Create a zip file with all encrypted files
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file_path in encrypted_files:
            if os.path.exists(file_path):
                zip_file.write(file_path, os.path.basename(file_path))
            else:
                print(f"File not found: {file_path}")
    zip_buffer.seek(0)

    return send_file(zip_buffer, as_attachment=True, download_name="encrypted_files.zip", mimetype='application/zip')

@app.route('/decrypt', methods=['POST'])
def decrypt_files():
    files = request.files.getlist('files')
    decrypted_files = []

    for file in files:
        filename = file.filename
        file_path = os.path.join('uploads', filename)

        # Save the encrypted file
        file.save(file_path)

        # Read the encrypted data
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()

        # Decrypt the data
        decrypted_data = cipher.decrypt(encrypted_data)

        # Save the decrypted file
        decrypted_file_path = os.path.join('decrypted', 'decrypted_' + filename)
        with open(decrypted_file_path, 'wb') as f:
            f.write(decrypted_data)

        decrypted_files.append(decrypted_file_path)

    # Create a zip file with all decrypted files
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file_path in decrypted_files:
            zip_file.write(file_path, os.path.basename(file_path))
    zip_buffer.seek(0)

    return send_file(zip_buffer, as_attachment=True, download_name="decrypted_files.zip", mimetype='application/zip')

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('encrypted', exist_ok=True)
    os.makedirs('decrypted', exist_ok=True)
    app.run(host='0.0.0.0')
