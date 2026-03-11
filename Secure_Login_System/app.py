"""
app.py - Main Flask application for the Secure Login System

KEY SECURITY CONCEPTS USED:
    1. PASSWORD HASHING   — bcrypt transforms the password into an unreadable digest.
    2. SALTING            — bcrypt automatically generates a unique random salt per
                           password, so two users with the same password get
                           completely different hashes. This defeats rainbow-table
                           attacks.
    3. WORK FACTOR        — The '12' in bcrypt(rounds=12) controls how slow the hash
                           computation is. Slower = harder to brute-force.
    4. NEVER STORE PLAIN TEXT — We discard the raw password immediately after hashing.

HOW bcrypt SALTING WORKS:
    Plain password:  "hunter2"
    Random salt:     "$2b$12$KIXoRzBl3J1u7oVDCexQfu"  (auto-generated)
    Final hash:      "$2b$12$KIXoRzBl3J1u7oVDCexQfuK6n8QwXz..."

    The salt is embedded IN the hash string, so bcrypt.checkpw() can
    re-derive it automatically during login verification.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import bcrypt
from database import init_db, add_user, get_user

app = Flask(__name__)

# Secret key used to sign the session cookie — change this to a random
# secret string in any real deployment (e.g. use os.urandom(24))
app.secret_key = "change-this-to-a-random-secret-in-production"


# ─────────────────────────────────────────────
#  REGISTRATION
# ─────────────────────────────────────────────

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    GET  → show the registration form
    POST → hash the password and save the new user
    """
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        # ── STEP 1: Validate inputs ──────────────────────────────────────
        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must be at least 8 characters.", "error")
            return redirect(url_for("register"))

        # ── STEP 2: Hash + salt the password with bcrypt ─────────────────
        #
        #   bcrypt.hashpw() does TWO things automatically:
        #     a) Generates a cryptographically random SALT
        #     b) Hashes the password combined with that salt
        #
        #   rounds=12 means 2^12 = 4096 iterations — slow enough to deter
        #   brute-force attacks, fast enough to not annoy real users.
        #
        #   The resulting hash looks like:
        #     b'$2b$12$<22-char-salt><31-char-hash>'
        #
        password_bytes  = password.encode("utf-8")          # str → bytes
        salt            = bcrypt.gensalt(rounds=12)          # random salt
        hashed_password = bcrypt.hashpw(password_bytes, salt) # hash it

        # ── STEP 3: Store ONLY the hash (never the plain password) ────────
        success = add_user(username, hashed_password)

        if success:
            flash("Account created! Please log in.", "success")
            return redirect(url_for("login"))
        else:
            flash("Username already taken. Try another.", "error")
            return redirect(url_for("register"))

    return render_template("register.html")


# ─────────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────────

@app.route("/login", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def login():
    """
    GET  → show the login form
    POST → verify credentials against the stored hash
    """
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        # ── STEP 1: Look up the user in the database ─────────────────────
        user = get_user(username)

        # ── STEP 2: Verify the password using bcrypt.checkpw() ───────────
        #
        #   bcrypt.checkpw() works by:
        #     a) Extracting the embedded salt from the stored hash
        #     b) Re-hashing the provided password with that same salt
        #     c) Comparing the result with the stored hash (constant-time
        #        comparison to prevent timing attacks)
        #
        #   We never decrypt the hash — it's mathematically impossible.
        #   We only CHECK whether the same input produces the same output.
        #
        if user:
            password_bytes   = password.encode("utf-8")
            stored_hash      = user["password"].encode("utf-8")  # str → bytes
            password_matches = bcrypt.checkpw(password_bytes, stored_hash)
        else:
            password_matches = False

        # ── STEP 3: Grant or deny access ─────────────────────────────────
        #
        #   IMPORTANT: We show the SAME error message whether the username
        #   is wrong OR the password is wrong. This prevents "username
        #   enumeration" — attackers finding out which usernames exist.
        #
        if password_matches:
            session["username"] = user["username"]
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


# ─────────────────────────────────────────────
#  DASHBOARD (protected page)
# ─────────────────────────────────────────────

@app.route("/dashboard")
def dashboard():
    """A simple protected page — only accessible when logged in."""
    if "username" not in session:
        flash("Please log in to access this page.", "error")
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])


# ─────────────────────────────────────────────
#  LOGOUT
# ─────────────────────────────────────────────

@app.route("/logout")
def logout():
    """Clear the session to log the user out."""
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    init_db()          # Create the DB/table if they don't exist yet
    app.run(host="0.0.0.0", port=8080, debug=True) # debug=True gives helpful error pages during development
                        # NEVER use debug=True in production!
