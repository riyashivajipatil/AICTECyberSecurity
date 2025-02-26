import cv2
import numpy as np
import time
import os

# ✅ Encryption Function
def encrypt_image(input_image_path, output_image_path, secret_message, passkey):
    img = cv2.imread(input_image_path)
    if img is None:
        print("\n❌ Error: Image not found!")
        return

    # Add a verification tag to the message before encryption
    tagged_message = "SECURE-" + secret_message  

    # Encrypt the message using XOR with passkey
    encrypted_message = "".join(chr(ord(char) ^ ord(passkey[i % len(passkey)])) for i, char in enumerate(tagged_message))
    encrypted_message += "þ"  # End delimiter

    binary_message = ''.join(format(ord(char), '08b') for char in encrypted_message)
    message_length = len(binary_message)

    rows, cols, channels = img.shape
    index = 0

    for row in range(rows):
        for col in range(cols):
            for channel in range(channels):  
                if index < message_length:
                    bit = int(binary_message[index])
                    img[row, col, channel] = (img[row, col, channel] & 254) | bit  
                    index += 1
                else:
                    break
            if index >= message_length:
                break
        if index >= message_length:
            break

    cv2.imwrite(output_image_path, img)
    print(f"\n✅ Secret message encrypted and saved as {output_image_path}")

# ✅ Decryption Function with Retry Option
def decrypt_image(image_path, correct_passkey):
    img = cv2.imread(image_path)
    if img is None:
        print("\n❌ Error: Image not found!")
        return None

    binary_message = ""
    rows, cols, channels = img.shape

    for row in range(rows):
        for col in range(cols):
            for channel in range(channels):
                binary_message += str(img[row, col, channel] & 1)

    # Convert binary to text
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    extracted_message = "".join(chr(int(char, 2)) for char in chars if int(char, 2) != 0)

    # Check for delimiter
    if "þ" not in extracted_message:
        print("\n❌ No hidden message found!")
        return None

    encrypted_message = extracted_message.split("þ")[0]  

    MAX_ATTEMPTS = 2
    LOCKOUT_TIME = 60  # seconds

    while True:
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            passkey = input("\nEnter the passkey for decryption: ")

            # Try to decrypt using the entered passkey
            decrypted_message = "".join(chr(ord(char) ^ ord(passkey[i % len(passkey)])) for i, char in enumerate(encrypted_message))

            # ✅ Validation Check: Message must start with "SECURE-"
            if decrypted_message.startswith("SECURE-"):
                final_message = decrypted_message.replace("SECURE-", "", 1)
                print("\n✅ Decryption Successful! The secret message is:\n📩", final_message)
                return
            else:
                print("\n❌ Invalid Passkey! Try again.")
                attempts += 1

        # Too many failed attempts - Lock for 60 seconds
        print("\n⏳ Too many incorrect attempts! Please wait 60 seconds before trying again.")
        time.sleep(LOCKOUT_TIME)

        # ✅ Ask if user wants to try again
        retry = input("\nDo you want to try again? (yes/no): ").strip().lower()
        if retry != "yes":
            print("\n🔒 Exiting the decryption process.")
            return

# ✅ File Paths (YOUR SPECIFIC PATHS)
input_image_path = r"C:\Users\Riya Shivaji Patil\Desktop\Sample img.webp"
output_image_path = r"C:\Users\Riya Shivaji Patil\Desktop\stego img\encrypted_image.png"

# ✅ Ask user if they want to encrypt
encrypt = input("Do you want to encrypt a message? (yes/no): ").strip().lower()
if encrypt == "yes":
    secret_message = input("Enter the secret message to hide: ")
    passkey = input("Enter a passkey for encryption: ")
    encrypt_image(input_image_path, output_image_path, secret_message, passkey)

# ✅ Ask user if they want to decrypt
decrypt = input("\nDo you want to decrypt an image? (yes/no): ").strip().lower()
if decrypt == "yes":
    decrypt_image(output_image_path, passkey)
