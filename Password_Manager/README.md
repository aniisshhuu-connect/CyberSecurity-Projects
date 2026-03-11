# Password Manager — Python Beginner Project

A simple command-line password manager built in Python.  
Stores your passwords in a local encrypted file using the `cryptography` library.

---

## 📁 Project Structure

```
password_manager/
├── main.py          # Main entry point — run this to use the app
├── crypto_utils.py  # Handles all encryption and decryption
├── storage.py       # Handles reading/writing vault.json
└── README.md        # This file
```

After first run, two new files will be created automatically:
```
├── vault.json       # Your encrypted passwords (created on first save)
└── salt.bin         # Cryptographic salt (created on first run)
```

> ⚠️ **Never delete `salt.bin`** — without it, your vault cannot be decrypted!

---

## ⚙️ Installation

### 1. Make sure Python is installed
```bash
python --version
# Should show Python 3.8 or higher
```

### 2. Install the required library
```bash
pip install cryptography
```

That's it — only one external dependency!

---

## ▶️ How to Run

Navigate to the project folder and run:

```bash
cd password_manager
python main.py
```

You'll be asked for a **master password** every time you start the app.  
The first time you run it, you choose your master password — remember it, because there's no recovery option!

---

## 💡 Example Usage

```
Welcome to your Password Manager!
Your passwords are encrypted with your master password.

🔐 Enter your master password: [hidden]

✓ Vault unlocked successfully!

=============================
       PASSWORD MANAGER      
=============================
  1. Add new credential
  2. View all credentials
  3. Delete a credential
  4. Quit
-----------------------------
  Choose an option (1-4): 1

--- Add New Credential ---
  Website/App name (e.g. github): github
  Username or email: johndoe@email.com
  Password to store: [hidden]
  ✓ Credentials for 'github' saved successfully.

  Choose an option (1-4): 2

--- Your Stored Credentials ---

  🌐 Site:     github
     Username: johndoe@email.com
     Password: mySecretPassword123
```

---

## 🔒 How Encryption Works (Simple Explanation)

This project uses **Fernet symmetric encryption** from the `cryptography` library.

Here's the process, step by step:

### Step 1 — Your master password → encryption key
Your master password can't be used directly as an encryption key.  
Instead, we use a technique called **PBKDF2** to turn it into a strong 32-byte key:

```
master_password + salt  →  PBKDF2 (480,000 rounds)  →  32-byte key
```

- The **salt** is a random value saved in `salt.bin`. It makes sure your key is unique even if someone else uses the same password.
- Running 480,000 rounds makes it extremely slow to guess passwords by brute force.

### Step 2 — Encrypting a password
```
plain password  +  key  →  Fernet.encrypt()  →  encrypted bytes
```
The encrypted bytes look like random gibberish and are stored in `vault.json`.

### Step 3 — Decrypting to view
```
encrypted bytes  +  key  →  Fernet.decrypt()  →  original password
```
When you view credentials, they are decrypted in memory and printed — never stored in plain text.

---

## 🗂️ What's Inside `vault.json`?

```json
{
    "github": {
        "username": "johndoe@email.com",
        "password": "gAAAAABmXk9z3v...encrypted gibberish...=="
    }
}
```

Even if someone opens this file, they can't read any passwords without your master password.

---

## ⚠️ Limitations (It's a Student Project!)

- **No master password recovery** — if you forget it, your vault is unrecoverable
- **No password generator** — you type passwords manually
- **No clipboard copy** — passwords print to screen
- **Local only** — no sync or cloud backup
- These would all be great features to add yourself! 🚀

---

## 🧠 What You'll Learn From This Project

- How symmetric encryption works
- What key derivation (PBKDF2) is and why it matters
- How to use Python's `cryptography` library
- Reading and writing JSON files
- Structuring a Python project across multiple files
- Hiding terminal input with `getpass`
