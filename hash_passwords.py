import bcrypt

passwords = ["password123", "qwerty"]

for plain in passwords:
    hashed = bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()
    print(f"Plain: {plain}\nHashed: {hashed}\n")
