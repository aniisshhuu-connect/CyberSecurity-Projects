# storage.py
# This file handles reading and writing the password vault to disk.
#
# The vault is stored as a JSON file called "vault.json".
# Each entry looks like this:
#
#   {
#     "github": {
#       "username": "john_doe",
#       "password": "<encrypted gibberish>"
#     },
#     ...
#   }
#
# Passwords are always stored encrypted. We only decrypt them
# when the user asks to view them (that happens in main.py).

import json
import os

# The name of the file where we store all passwords
VAULT_FILE = "vault.json"


def load_vault() -> dict:
    """
    Load and return the vault dictionary from the JSON file.
    If the vault file doesn't exist yet, return an empty dictionary.
    """
    if not os.path.exists(VAULT_FILE):
        # First time running — no vault exists yet
        return {}

    with open(VAULT_FILE, "r") as f:
        vault = json.load(f)

    return vault


def save_vault(vault: dict):
    """
    Save the vault dictionary to the JSON file.
    We use indent=4 to make the file human-readable (useful for debugging).
    Note: even though the file is readable, passwords are still encrypted inside it.
    """
    with open(VAULT_FILE, "w") as f:
        json.dump(vault, f, indent=4)


def add_credential(site: str, username: str, encrypted_password: str):
    """
    Add a new entry to the vault.
    The password should already be encrypted before calling this function.
    """
    vault = load_vault()

    # Store using the site name as the key
    vault[site] = {
        "username": username,
        "password": encrypted_password
    }

    save_vault(vault)
    print(f"  ✓ Credentials for '{site}' saved successfully.")


def get_all_credentials() -> dict:
    """
    Return all entries from the vault.
    Passwords are still encrypted at this point.
    """
    return load_vault()


def delete_credential(site: str) -> bool:
    """
    Delete an entry from the vault by site name.
    Returns True if the entry was found and deleted, False if it wasn't found.
    """
    vault = load_vault()

    if site not in vault:
        return False  # Entry doesn't exist

    del vault[site]
    save_vault(vault)
    return True
