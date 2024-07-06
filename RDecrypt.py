import os
from Crypto.Cipher import AES
import base64

class Decryption:
    def __init__(self, key):
        self.key = key

    def unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

    def decrypt_file(self, file_path):
        print(f"Attempting to decrypt {file_path}")
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        try:
            # Read the encrypted file
            with open(file_path, 'rb') as file:
                encrypted = file.read()
            print(f"Encrypted content of {file_path}: {encrypted}")

            # Decode the base64 encoded data
            encrypted = base64.b64decode(encrypted)
            iv = encrypted[:AES.block_size]
            
            # Create a cipher object and decrypt the data
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted = self.unpad(cipher.decrypt(encrypted[AES.block_size:])).decode('utf-8')
            print(f"Decrypted content: {decrypted}")

            # Write the decrypted content back to the file
            with open(file_path, 'w') as file:
                file.write(decrypted)
            print(f"Decrypted content written to {file_path}")

            # Verify the file has been changed
            with open(file_path, 'r') as file:
                final_content = file.read()
            print(f"Final content of {file_path}: {final_content}")

        except Exception as e:
            print(f"Error decrypting {file_path}: {e}")

    def decrypt_files_in_directory(self, directory):
        print(f"Starting decryption for directory: {directory}")
        if os.path.isfile(directory):
            self.decrypt_file(directory)
        else:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.decrypt_file(file_path)
        print("Decryption process completed.")

# Example usage
key = b'Sixteen byte key'  # Ensure this key is the same as the one used for encryption
file_to_decrypt = 'SuperSecretFile.txt'  # Replace with the path to your file
decryption = Decryption(key)
decryption.decrypt_files_in_directory(file_to_decrypt)
