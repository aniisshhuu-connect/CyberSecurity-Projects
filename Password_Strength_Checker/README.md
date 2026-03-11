# Password Strength Checker

A beginner-friendly **cybersecurity mini project** built with Python.  
It uses **Regular Expressions (Regex)** to analyze passwords and classify them as Weak, Medium, or Strong.

---

## 📁 Project Structure

```
password_checker/
├── checker.py    ← Main program
└── README.md     ← This file
```

---

## 🚀 How to Run

```bash
python checker.py
```

No external libraries needed — only Python's built-in `re` module!

---

## ✅ What It Checks

| Criterion                | Points |
|--------------------------|--------|
| Length ≥ 8 characters    | +1     |
| Length ≥ 12 characters   | +1     |
| Has an uppercase letter  | +1     |
| Has a lowercase letter   | +1     |
| Has a digit (0–9)        | +1     |
| Has a special character  | +2     |
| **Maximum Score**        | **7**  |

### 🏷️ Strength Labels

| Score | Label  |
|-------|--------|
| 0–2   | 🔴 Weak   |
| 3–4   | 🟡 Medium |
| 5–7   | 🟢 Strong |

---

## 🔍 Regex Patterns Used

```python
r'[A-Z]'     # Matches any uppercase letter
r'[a-z]'     # Matches any lowercase letter
r'[0-9]'     # Matches any digit
r'[!@#$%^&*(),.?":{}|<>_\-\[\]\/\\+=;\'`~]'  # Matches special chars
```

`re.search(pattern, string)` returns a match if the pattern is found **anywhere** in the string.  
`bool(...)` converts the result to `True` (found) or `False` (not found).

---

## 💡 Example Inputs & Outputs

### Example 1 — Weak Password: `abc`
```
==================================================
       🔐 PASSWORD STRENGTH REPORT
==================================================
  Password : ***  (3 characters)
  Score    : [░░░░░░░] 0/7
  Strength : 🔴  Weak
--------------------------------------------------
  CHECKLIST:
    ❌  At least 8 characters
    ❌  At least 12 characters (bonus)
    ❌  Uppercase letter
    ✅  Lowercase letter
    ❌  Number
    ❌  Special character
--------------------------------------------------
  💡 SUGGESTIONS TO IMPROVE:
    📏  Make it at least 8 characters long.
    🔠  Add at least one UPPERCASE letter (e.g. A, B, C ...).
    🔢  Include at least one number (e.g. 1, 2, 3 ...).
    ✨  Add a special character (e.g. @, #, $, !, _ ...).
==================================================
```

### Example 2 — Medium Password: `Hello123`
```
==================================================
       🔐 PASSWORD STRENGTH REPORT
==================================================
  Password : ********  (8 characters)
  Score    : [████░░░] 4/7
  Strength : 🟡  Medium
--------------------------------------------------
  CHECKLIST:
    ✅  At least 8 characters
    ❌  At least 12 characters (bonus)
    ✅  Uppercase letter
    ✅  Lowercase letter
    ✅  Number
    ❌  Special character
--------------------------------------------------
  💡 SUGGESTIONS TO IMPROVE:
    📏  Consider making it 12+ characters for extra security.
    ✨  Add a special character (e.g. @, #, $, !, _ ...).
==================================================
```

### Example 3 — Strong Password: `MyS3cur3P@ss!`
```
==================================================
       🔐 PASSWORD STRENGTH REPORT
==================================================
  Password : *************  (13 characters)
  Score    : [███████] 7/7
  Strength : 🟢  Strong
--------------------------------------------------
  CHECKLIST:
    ✅  At least 8 characters
    ✅  At least 12 characters (bonus)
    ✅  Uppercase letter
    ✅  Lowercase letter
    ✅  Number
    ✅  Special character
--------------------------------------------------
  🎉  Your password meets all criteria. Great job!
==================================================
```

---

## 🧠 Key Concepts Learned

- **Regular Expressions (Regex)** — pattern matching inside strings
- **Functions** — breaking code into small, reusable pieces
- **Loops & Conditionals** — control flow in Python
- **String methods** — `len()`, `.strip()`, `.lower()`
- **Cybersecurity awareness** — what makes a password strong

---

## 🔒 Password Tips

> A strong password should be **long**, **random**, and **unique** for every account.  
> Consider using a **password manager** (e.g. Bitwarden, 1Password) to generate and store them safely.
