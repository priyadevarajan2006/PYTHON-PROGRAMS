import hashlib
text="SecureData123"
hashed=hashlib.sha256(text.encode()).hexdigest()
print(f"SHA-256 hash:{hashed}")
