# 🔐 Secure Login System — Flask + bcrypt + SQLite

A college cybersecurity project demonstrating **salted password hashing**,
**secure authentication**, and **safe credential storage**.

---

## Project Structure

```
secure_login/
├── app.py           # Flask routes: register, login, logout, dashboard
├── database.py      # SQLite setup and user CRUD helpers
├── requirements.txt # Python dependencies
└── templates/
    ├── login.html      # Login page
    ├── register.html   # Registration page (with password strength meter)
    └── dashboard.html  # Protected page shown after login
```

---

## Database Schema

```sql
CREATE TABLE users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT    NOT NULL UNIQUE,
    password TEXT    NOT NULL        -- bcrypt hash string, e.g.:
                                     -- $2b$12$KIXoRzBl3J1u7oVDCexQfu...
);
```

**Why `password` is a hash, not the real password:**
- If the database is stolen, attackers see only unreadable hashes
- bcrypt is intentionally slow — brute-forcing millions of guesses takes years
- Each user's hash is unique thanks to the random salt

---

## Setup Instructions

### 1. Clone / download the project

```bash
cd secure_login
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Activate it:
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install flask bcrypt
```

### 4. Run the app

```bash
python app.py
```

You should see:
```
[DB] Database initialized — users table ready.
 * Running on http://127.0.0.1:5000
```

### 5. Open in your browser

- **Register:** http://127.0.0.1:5000/register
- **Login:**    http://127.0.0.1:5000/login

---

## Security Concepts Explained

### Why plain-text passwords are dangerous
If you store `password = "hunter2"` and your database leaks, every user's
account is instantly compromised — including on other sites where they reuse
the same password. This has happened to real companies (LinkedIn 2012, Adobe
2013, RockYou 2009).

### What is hashing?
A hash function (like SHA-256 or bcrypt) converts input into a fixed-length
string that **cannot be reversed**. `bcrypt("hunter2") → $2b$12$...` but
you can never go backwards from the hash to "hunter2".

### What is salting?
A **salt** is a random string added to the password before hashing.
Without salts, two users with the same password produce the same hash —
making **rainbow table attacks** trivial. With salts:

```
alice  + salt_A → hash_X
bob    + salt_B → hash_Y   ← completely different, even if passwords match
```

bcrypt embeds the salt inside the hash string automatically.

### What is bcrypt's work factor?
`bcrypt.gensalt(rounds=12)` means 2^12 = 4096 hash iterations.
This makes each hash take ~100ms on modern hardware. For a real user logging
in, 100ms is imperceptible. For an attacker trying billions of guesses, it
makes brute-force attacks computationally infeasible.

---

## Example: What's actually stored in the DB

| id | username | password                                           |
|----|----------|----------------------------------------------------|
| 1  | alice    | $2b$12$KIXoRzBl3J1u7oVDCexQfuK6n8QwXzAbCdEfGhIj  |
| 2  | bob      | $2b$12$MnOpQrStUvWxYz01234567890abcdefghijklmnop  |

The hash string encodes: `$2b` (algorithm) `$12` (rounds) `$<22-char-salt><31-char-hash>`

---

## Production Checklist (beyond this demo)

- [ ] Replace `app.secret_key` with `os.urandom(24)` stored securely
- [ ] Use HTTPS (TLS) in production
- [ ] Add rate limiting to `/login` to prevent brute-force
- [ ] Set `debug=False` when deploying
- [ ] Consider adding CSRF protection (e.g. Flask-WTF)
