import bcrypt

# Replace these with your chosen plaintext passwords
passwords = ["password123", "qwerty"]

for pw in passwords:
    hashed = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
    print(f"Plain: {pw}")
    print(f"Hashed: {hashed.decode()}\n")
