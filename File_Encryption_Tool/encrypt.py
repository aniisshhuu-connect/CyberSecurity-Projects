import sys
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from key_manager import load_key


def encrypt_file(filepath):
    """
    Encrypts a single file and saves it as <filepath>.enc

    Parameters:
        filepath (str): Path to the file you want to encrypt

    What we store in the .enc file (in order):
        [12 bytes nonce] + [encrypted data + 16 byte auth tag]
    """

    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: '{filepath}'")
        print("[!] Double-check the filename and try again.")
        return

    print(f"[*] Loading encryption key...")
    key = load_key()

    # --- Step 3: Create an AES-GCM cipher object using our key ---
    aesgcm = AESGCM(key)

    # --- Step 4: Generate a random nonce ---
    # WHAT IS A NONCE?
    #   Nonce = "Number used ONCE"
    #   It's a random value mixed into the encryption so that encrypting
    #   the SAME file twice produces DIFFERENT output each time.
    #   Without a nonce, attackers could detect when two files have the
    #   same content — a serious privacy leak!
    #
    #   For AES-GCM, the nonce should be 12 bytes (96 bits).
    nonce = os.urandom(12)
    print(f"[*] Generated random nonce (12 bytes)")

    # --- Step 5: Read the original file ---
    print(f"[*] Reading file: {filepath}")
    with open(filepath, "rb") as f:
        plaintext = f.read()
    print(f"[*] File size: {len(plaintext)} bytes")

    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    output_path = filepath + ".enc"
    with open(output_path, "wb") as f:
        f.write(nonce + ciphertext)

    print(f"\n[+] SUCCESS! File encrypted.")
    print(f"[+] Saved as: {output_path}")
    print(f"[+] Encrypted size: {len(nonce) + len(ciphertext)} bytes")
    print(f"\n[TIP] To decrypt: python decrypt.py {output_path}")
    print(f"[TIP] You can now safely delete the original: {filepath}")


if __name__ == "__main__":
    print("=" * 50)
    print("   FILE ENCRYPTOR — AES-256-GCM")
    print("=" * 50)

    if len(sys.argv) != 2:
        print("\n[ERROR] Please provide a file to encrypt.")
        print("Usage:  python encrypt.py <filename>")
        print("Example: python encrypt.py myfile.txt")
        sys.exit(1)

    filename = sys.argv[1]
    encrypt_file(filename)
