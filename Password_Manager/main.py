# main.py
# This is the main file you run to use the password manager.
# It handles the user interface (text menu) and ties together
# the crypto and storage modules.
#
# Run this with:  python main.py

import getpass  # Used to hide password input (like sudo in terminal)
from cryptography.fernet import InvalidToken

# Import our own modules
import crypto_utils
import storage


def prompt_master_password() -> str:
    """
    Ask the user to enter their master password.
    getpass.getpass() hides what they type — good for security!
    """
    password = getpass.getpass("🔐 Enter your master password: ")
    return password


def verify_master_password(master_password: str) -> bool:
    """
    Try to verify the master password is correct by attempting
    to decrypt one stored password.

    If the vault is empty, we can't verify — just trust it.
    If decryption fails (InvalidToken error), the password is wrong.
    """
    vault = storage.get_all_credentials()

    if not vault:
        # Nothing stored yet, can't verify — that's okay for first use
        return True

    # Try to decrypt the first entry in the vault as a test
    first_site = list(vault.keys())[0]
    encrypted_pw = vault[first_site]["password"]

    try:
        crypto_utils.decrypt_password(encrypted_pw, master_password)
        return True  # Decryption worked — correct password!
    except InvalidToken:
        return False  # Wrong master password


def add_new_credential(master_password: str):
    """
    Ask the user for a site, username, and password,
    encrypt the password, then save everything to the vault.
    """
    print("\n--- Add New Credential ---")
    site = input("  Website/App name (e.g. github): ").strip().lower()

    if not site:
        print("  ✗ Site name can't be empty.")
        return

    username = input("  Username or email: ").strip()
    password = getpass.getpass("  Password to store: ")

    if not password:
        print("  ✗ Password can't be empty.")
        return

    # Encrypt the password before storing it
    encrypted = crypto_utils.encrypt_password(password, master_password)

    # Save to vault
    storage.add_credential(site, username, encrypted)


def view_credentials(master_password: str):
    """
    Load all credentials from the vault, decrypt each password,
    and display them to the user.
    """
    print("\n--- Your Stored Credentials ---")

    vault = storage.get_all_credentials()

    if not vault:
        print("  (No credentials stored yet.)")
        return

    # Loop through each saved entry
    for site, data in vault.items():
        username = data["username"]
        encrypted_pw = data["password"]

        # Decrypt the password so we can show it
        try:
            plain_pw = crypto_utils.decrypt_password(encrypted_pw, master_password)
        except Exception:
            plain_pw = "[error decrypting]"

        # Display the entry
        print(f"\n  🌐 Site:     {site}")
        print(f"     Username: {username}")
        print(f"     Password: {plain_pw}")

    print()  # Blank line at the end for readability


def delete_credential():
    """
    Ask the user which site to delete, then remove it from the vault.
    """
    print("\n--- Delete a Credential ---")
    site = input("  Enter the site name to delete: ").strip().lower()

    if not site:
        print("  ✗ Site name can't be empty.")
        return

    success = storage.delete_credential(site)

    if success:
        print(f"  ✓ '{site}' deleted.")
    else:
        print(f"  ✗ No entry found for '{site}'.")


def show_menu():
    """
    Print the main menu options.
    """
    print("\n=============================")
    print("       PASSWORD MANAGER      ")
    print("=============================")
    print("  1. Add new credential")
    print("  2. View all credentials")
    print("  3. Delete a credential")
    print("  4. Quit")
    print("-----------------------------")


def main():
    """
    Entry point of the app.
    1. Ask for master password
    2. Verify it (if vault has existing data)
    3. Show menu loop
    """
    print("\nWelcome to your Password Manager!")
    print("Your passwords are encrypted with your master password.\n")

    # Step 1: Get master password from user
    master_password = prompt_master_password()

    # Step 2: Verify the password against existing data
    if not verify_master_password(master_password):
        print("\n✗ Incorrect master password. Exiting.")
        return

    print("\n✓ Vault unlocked successfully!")

    # Step 3: Main menu loop
    while True:
        show_menu()
        choice = input("  Choose an option (1-4): ").strip()

        if choice == "1":
            add_new_credential(master_password)

        elif choice == "2":
            view_credentials(master_password)

        elif choice == "3":
            delete_credential()

        elif choice == "4":
            print("\nGoodbye! Stay secure. 🔒\n")
            break

        else:
            print("  ✗ Invalid choice. Please enter 1, 2, 3, or 4.")


# Only run main() if this file is executed directly
# (not if it's imported by another file)
if __name__ == "__main__":
    main()
