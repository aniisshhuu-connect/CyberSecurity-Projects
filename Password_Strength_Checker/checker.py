import re

UPPERCASE_PATTERN   = r'[A-Z]'
LOWERCASE_PATTERN   = r'[a-z]'
DIGIT_PATTERN       = r'[0-9]'
SPECIAL_CHAR_PATTERN = r'[!@#$%^&*(),.?":{}|<>_\-\[\]\/\\+=;\'`~]'

def analyze_password(password):
    """
    Checks the password against all criteria.
    Returns a dictionary with True/False for each check.
    """
    results = {
        "long_enough":    len(password) >= 8,
        "very_long":      len(password) >= 12,
        "has_uppercase":  bool(re.search(UPPERCASE_PATTERN,    password)),
        "has_lowercase":  bool(re.search(LOWERCASE_PATTERN,    password)),
        "has_digit":      bool(re.search(DIGIT_PATTERN,        password)),
        "has_special":    bool(re.search(SPECIAL_CHAR_PATTERN, password)),
    }
    return results

def calculate_score(results):
    """
    Assigns a numeric score (0–7) based on which criteria are met.
    Each criterion is worth 1 point, with a bonus for very long passwords.
    """
    score = 0
    if results["long_enough"]:   score += 1
    if results["very_long"]:     score += 1
    if results["has_uppercase"]: score += 1
    if results["has_lowercase"]: score += 1
    if results["has_digit"]:     score += 1
    if results["has_special"]:   score += 2
    return score

def classify_password(score):
    """
    Converts the numeric score into a human-readable strength label.
    """
    if score <= 2:
        return "Weak",   "🔴"
    elif score <= 4:
        return "Medium", "🟡"
    else:
        return "Strong", "🟢"

def get_suggestions(results):
    """
    Looks at which checks FAILED and returns helpful tips.
    Returns an empty list if no improvements are needed.
    """
    tips = []

    if not results["long_enough"]:
        tips.append("📏  Make it at least 8 characters long.")
    elif not results["very_long"]:
        tips.append("📏  Consider making it 12+ characters for extra security.")

    if not results["has_uppercase"]:
        tips.append("🔠  Add at least one UPPERCASE letter (e.g. A, B, C ...).")

    if not results["has_lowercase"]:
        tips.append("🔡  Add at least one lowercase letter (e.g. a, b, c ...).")

    if not results["has_digit"]:
        tips.append("🔢  Include at least one number (e.g. 1, 2, 3 ...).")

    if not results["has_special"]:
        tips.append("✨  Add a special character (e.g. @, #, $, !, _ ...).")

    return tips

def display_results(password, results, score, label, icon, suggestions):
    """
    Prints a nicely formatted report for the user.
    """
    bar_filled = "█" * score
    bar_empty  = "░" * (7 - score)
    strength_bar = f"[{bar_filled}{bar_empty}] {score}/7"

    print("\n" + "=" * 50)
    print("       🔐 PASSWORD STRENGTH REPORT")
    print("=" * 50)
    print(f"  Password : {'*' * len(password)}  ({len(password)} characters)")
    print(f"  Score    : {strength_bar}")
    print(f"  Strength : {icon}  {label}")
    print("-" * 50)
    print("  CHECKLIST:")
    print(f"    {'✅' if results['long_enough']   else '❌'}  At least 8 characters")
    print(f"    {'✅' if results['very_long']      else '❌'}  At least 12 characters (bonus)")
    print(f"    {'✅' if results['has_uppercase']  else '❌'}  Uppercase letter")
    print(f"    {'✅' if results['has_lowercase']  else '❌'}  Lowercase letter")
    print(f"    {'✅' if results['has_digit']      else '❌'}  Number")
    print(f"    {'✅' if results['has_special']    else '❌'}  Special character")

    if suggestions:
        print("-" * 50)
        print("  💡 SUGGESTIONS TO IMPROVE:")
        for tip in suggestions:
            print(f"    {tip}")
    else:
        print("-" * 50)
        print("  🎉  Your password meets all criteria. Great job!")

    print("=" * 50 + "\n")

def main():
    print("\n╔══════════════════════════════════════╗")
    print("║   🔑  Password Strength Checker      ║")
    print("╚══════════════════════════════════════╝")
    print("  Type 'quit' at any time to exit.\n")

    while True:
        password = input("  Enter a password to check: ").strip()

        if password.lower() == "quit":
            print("\n  👋  Goodbye! Stay secure!\n")
            break

        if not password:
            print("  ⚠️   Please enter a password (it cannot be empty).\n")
            continue

        results     = analyze_password(password)
        score       = calculate_score(results)
        label, icon = classify_password(score)
        suggestions = get_suggestions(results)

        display_results(password, results, score, label, icon, suggestions)

        again = input("  Check another password? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("\n  👋  Goodbye! Stay secure!\n")
            break
        print()


if __name__ == "__main__":
    main()
