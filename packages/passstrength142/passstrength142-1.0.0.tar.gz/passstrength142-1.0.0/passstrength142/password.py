import requests
import hashlib
import string
import random

def check_password_strength(password):
    # Check if password has been involved in a data breach using the haveibeenpwned API
    sha1_password = hashlib.sha1(password.encode()).hexdigest().upper()
    sha1_prefix = sha1_password[:5]
    sha1_suffix = sha1_password[5:]
    url = f"https://api.pwnedpasswords.com/range/{sha1_prefix}"
    response = requests.get(url)
    if response.status_code != 200:
        print("Could not check password strength. Please try again later.")
        return
    
    hashes = [line.split(":") for line in response.text.splitlines()]
    for h, count in hashes:
        if h == sha1_suffix:
            print("Password has been involved in a data breach. Please choose a different password.")
            return
    
    # Calculate password strength
    length_score = min(len(password) // 4, 4) * 10
    upper_score = 10 if any(c.isupper() for c in password) else 0
    lower_score = 10 if any(c.islower() for c in password) else 0
    digit_score = 10 if any(c.isdigit() for c in password) else 0
    symbol_score = 10 if any(c in string.punctuation for c in password) else 0
    total_score = length_score + upper_score + lower_score + digit_score + symbol_score
    
    # Print password strength
    if total_score >= 80:
        print("Password is very strong.")
    elif total_score >= 60:
        print("Password is strong.")
    elif total_score >= 40:
        print("Password is moderately strong.")
    else:
        print("Password is weak.")
        
def generate_random_password(length=10):
    # Generate a random password of given length
    chars = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(chars) for _ in range(length))


