# File Encryption Tool
### A beginner Python cybersecurity project using AES-256-GCM

---

## 📚 What I Learned Building This

This project taught me how real encryption works under the hood. Instead of just *using* a password manager or encrypted drive, I actually understand *why* files are secure now.

Key concepts I learned:
- **AES-256** — the gold standard symmetric encryption algorithm
- **GCM mode** — authenticated encryption that detects tampering
- **Nonces** — why you can never reuse the same random value twice
- **Key management** — the hardest part of real-world cryptography

---

## 🛠️ Setup

**1. Install the dependency:**
```bash
pip install cryptography
```

**2. Generate your encryption key (do this FIRST):**
```bash
python key_manager.py
```
This creates a `secret.key` file. **Guard this file with your life.** Without it, your encrypted files are unrecoverable.

---

## 🚀 How to Use

**Encrypt a file:**
```bash
python encrypt.py myfile.txt
# Output: myfile.txt.enc
```

**Decrypt a file:**
```bash
python decrypt.py myfile.txt.enc
# Output: myfile.txt (restored)
```

---

## 📁 Project Structure

```
file_encryptor/
│
├── key_manager.py   # Generates and loads the AES-256 key
├── encrypt.py       # Encrypts files using AES-GCM
├── decrypt.py       # Decrypts .enc files
├── secret.key       # Generated key file (DO NOT SHARE THIS!)
└── README.md        # This file
```

---

## 🔬 How It Works (The Technical Stuff)

### AES-256-GCM Explained Simply

```
Original File  →  [AES-GCM + Key + Nonce]  →  Encrypted File (.enc)
     🔓                    🔑                         🔒
```

**Three things make this secure:**

| Component | What it does | Why it matters |
|-----------|-------------|----------------|
| **AES-256** | Scrambles data in 14 rounds of math | Brute-forcing a 256-bit key would take longer than the age of the universe |
| **GCM mode** | Adds a 16-byte authentication tag | Detects if anyone modified the encrypted file |
| **Nonce** | Random 12-byte value mixed into encryption | Ensures encrypting the same file twice gives different output |

### What's inside a `.enc` file?

```
[  12 bytes  ][        rest of file        ]
[   nonce    ][ ciphertext + 16-byte tag   ]
```

The nonce is **not secret** — it's stored in plain sight. That's okay! Its only job is to be unique, not hidden.

---

## 🌍 Real World Cybersecurity Connections

This toy project mirrors how real security systems work:

| This Project | Real World Equivalent |
|---|---|
| `secret.key` file | AWS KMS / Azure Key Vault |
| AES-256-GCM | Signal messenger, HTTPS (TLS 1.3), FileVault, BitLocker |
| Auth tag verification | Prevents ransomware from corrupting your backups silently |
| Nonce generation | Same concept used in TLS handshakes |

### Where you'll see AES-GCM in the wild:
- 🌐 **HTTPS** — Every website you visit uses AES-GCM to encrypt traffic
- 💬 **Signal / WhatsApp** — End-to-end encrypted messages
- 💾 **Full-disk encryption** — macOS FileVault, Windows BitLocker
- ☁️ **Cloud storage** — AWS S3 server-side encryption
- 🔑 **Password managers** — 1Password, Bitwarden

---

## ⚠️ Security Limitations (What a Real App Would Do Differently)

This is a **learning project**, not production software. Here's what's missing:

1. **Key stored in plaintext** → Real apps use password-derived keys (PBKDF2/Argon2) or hardware security modules
2. **No key rotation** → Production systems periodically generate new keys
3. **Original file not wiped** → Secure deletion requires overwriting with random data (just deleting leaves file recoverable)
4. **Single key for all files** → Real systems often use per-file keys wrapped by a master key

---

## 💡 Challenge Ideas (If you want to go further!)

- [ ] Add password-based key derivation (so you type a password instead of using a key file)
- [ ] Encrypt entire directories recursively
- [ ] Add a GUI using `tkinter`
- [ ] Implement secure file deletion (overwrite before deleting)
- [ ] Add support for encrypting with a public key (asymmetric — RSA or ECC)

---

*Built as a cybersecurity learning project. Uses Python's `cryptography` library (pyca/cryptography).*
