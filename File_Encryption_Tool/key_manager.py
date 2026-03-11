import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

KEY_FILE = "secret.key"


def generate_key():
    """
    Generates a secure 256-bit AES encryption key using os.urandom().

    WHY 256-BIT?
        AES-256 means our key is 256 bits (32 bytes) long.
        The more bits, the harder it is to guess by brute force.
        AES-256 is considered military-grade encryption — the same standard
        used to protect classified government data!

    WHY os.urandom()?
        os.urandom() asks the operating system for truly random bytes.
        This is much safer than random.random() which is predictable.
        Predictable keys = bad security!
    """
    key = os.urandom(32)
    return key


def save_key(key, filepath=KEY_FILE):
    """
    Saves the encryption key to a file.

    REAL WORLD WARNING:
        Storing a key in a plain file is risky in production!
        Anyone with access to the file system can steal your key.
        Real apps use:
          - Password-protected keystores
          - Hardware Security Modules (HSMs)
          - Cloud key management services (AWS KMS, Azure Key Vault)
    """
    with open(filepath, "wb") as key_file:
        key_file.write(key)
    print(f"[+] Key saved to: {filepath}")
    print("[!] WARNING: Keep this file safe! Anyone with this key can decrypt your files.")


def load_key(filepath=KEY_FILE):
    """
    Loads the encryption key from a file.

    If the key file doesn't exist, we tell the user — because without
    the original key, decryption is impossible!
    """
    if not os.path.exists(filepath):
        print(f"[ERROR] Key file '{filepath}' not found!")
        print("[!] You need the original key to decrypt files. Did you delete it?")
        exit(1)

    with open(filepath, "rb") as key_file:
        key = key_file.read()

    return key


if __name__ == "__main__":
    print("=" * 50)
    print("   FILE ENCRYPTOR — Key Generator")
    print("=" * 50)

    if os.path.exists(KEY_FILE):
        print(f"[!] A key already exists at '{KEY_FILE}'.")
        answer = input("    Overwrite it? (yes/no): ").strip().lower()
        if answer != "yes":
            print("[-] Key generation cancelled. Your old key is safe.")
            exit(0)

    # Generate and save a new key
    key = generate_key()
    save_key(key)

    print("\n[+] New encryption key generated successfully!")
    print(f"[+] Key length: {len(key) * 8} bits (AES-256)")
    print("\n[TIP] Run encrypt.py to start encrypting files.")
