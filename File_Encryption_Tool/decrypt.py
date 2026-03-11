import sys
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
from key_manager import load_key


def decrypt_file(filepath):
    """
    Decrypts a .enc file and restores the original file.

    Parameters:
        filepath (str): Path to the .enc file you want to decrypt
    """

    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: '{filepath}'")
        return

    if not filepath.endswith(".enc"):
        print(f"[WARNING] File doesn't have .enc extension: '{filepath}'")
        print("[!] Are you sure this was encrypted by this tool?")
        answer = input("    Continue anyway? (yes/no): ").strip().lower()
        if answer != "yes":
            return

    print(f"[*] Loading encryption key...")
    key = load_key()

    # --- Step 3: Create AES-GCM cipher with our key ---
    aesgcm = AESGCM(key)

    # --- Step 4: Read the encrypted file ---
    print(f"[*] Reading encrypted file: {filepath}")
    with open(filepath, "rb") as f:
        file_data = f.read()

    # --- Step 5: Split the nonce from the ciphertext ---
    # Remember from encrypt.py: we saved [nonce (12 bytes)] + [ciphertext]
    # So the first 12 bytes are our nonce, the rest is ciphertext + auth tag
    nonce = file_data[:12]        # First 12 bytes
    ciphertext = file_data[12:]
    print(f"[*] Extracted nonce and ciphertext")

    print(f"[*] Decrypting and verifying integrity...")
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    except InvalidTag:
        print("\n[ERROR] Decryption FAILED!")
        print("[!] Possible reasons:")
        print("    1. You're using the wrong key (wrong secret.key file)")
        print("    2. The encrypted file was corrupted or modified")
        print("    3. This file wasn't encrypted by this tool")
        print("\n[!] SECURITY NOTE: AES-GCM detected that something is wrong.")
        print("    This protects you from tampered or corrupted files!")
        return

    if filepath.endswith(".enc"):
        output_path = filepath[:-4]
    else:
        output_path = filepath + ".decrypted"

    if os.path.exists(output_path):
        print(f"\n[WARNING] '{output_path}' already exists.")
        answer = input("    Overwrite it? (yes/no): ").strip().lower()
        if answer != "yes":
            print("[-] Decryption cancelled. No files were changed.")
            return

    with open(output_path, "wb") as f:
        f.write(plaintext)

    print(f"\n[+] SUCCESS! File decrypted and verified.")
    print(f"[+] Restored file: {output_path}")
    print(f"[+] File size: {len(plaintext)} bytes")


if __name__ == "__main__":
    print("=" * 50)
    print("   FILE DECRYPTOR — AES-256-GCM")
    print("=" * 50)

    if len(sys.argv) != 2:
        print("\n[ERROR] Please provide a file to decrypt.")
        print("Usage:   python decrypt.py <filename.enc>")
        print("Example: python decrypt.py myfile.txt.enc")
        sys.exit(1)

    filename = sys.argv[1]
    decrypt_file(filename)
