import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

SALT_FILE = "salt.bin"


def load_or_create_salt():
    """Load the salt from disk, or create a new one if it doesn't exist."""
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()
    else:
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
        return salt


def derive_key(master_password: str) -> bytes:
    """Turn the master password string into a valid Fernet encryption key."""
    salt = load_or_create_salt()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key


def get_fernet(master_password: str) -> Fernet:
    """Create and return a Fernet object using the master password."""
    key = derive_key(master_password)
    return Fernet(key)


def encrypt_password(plain_password: str, master_password: str) -> str:
    """Encrypt a single password string."""
    f = get_fernet(master_password)
    encrypted_bytes = f.encrypt(plain_password.encode())
    return encrypted_bytes.decode()


def decrypt_password(encrypted_password: str, master_password: str) -> str:
    """Decrypt a previously encrypted password."""
    f = get_fernet(master_password)
    decrypted_bytes = f.decrypt(encrypted_password.encode())
    return decrypted_bytes.decode()
