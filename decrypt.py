def decrypt_image(encrypted_path, key):
    with open(encrypted_path, 'rb') as file:
        encrypted_data = file.read()

    # Extract the initialization vector
    iv = encrypted_data[:16]
    encrypted_image_data = encrypted_data[16:]

    # Create cipher object and decryptor
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt and unpad the data
    padded_data = decryptor.update(encrypted_image_data) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    image_data = unpadder.update(padded_data) + unpadder.finalize()
    
    return image_data

def save_decrypted_image(image_data, output_path, original_size):
    image = Image.frombytes('RGB', original_size, image_data)
    image.save(output_path)

decrypted_data = decrypt_image(output_path, key)
image = Image.open(image_path)
save_decrypted_image(decrypted_data, 'decrypted_image.jpg', image.size)
