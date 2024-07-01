from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from PIL import Image
import os

def encrypt_image(image_path, key):
    # Open the image
    with Image.open(image_path) as image:
        image_data = image.tobytes()

    # Generate a random initialization vector
    iv = os.urandom(16)
    
    # Create cipher object and encryptor
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad image data to be a multiple of block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(image_data) + padder.finalize()
    
    # Encrypt the padded data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv + encrypted_data

def save_encrypted_image(encrypted_data, output_path):
    with open(output_path, 'wb') as file:
        file.write(encrypted_data)

key = os.urandom(32)  # Generate a random key
image_path = 'path_to_image.jpg'
output_path = 'encrypted_image.enc'

encrypted_data = encrypt_image(image_path, key)
save_encrypted_image(encrypted_data, output_path)
