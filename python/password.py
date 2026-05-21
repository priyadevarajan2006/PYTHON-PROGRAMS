
import secrets
import string
alphabet = string.ascii_letters + string.digits + string.punctuation
# Generate a secure 12-character password
password = ''.join(secrets.choice(alphabet) for i in range(100))
print(f"[+] Generated Secure Password: {password}")

