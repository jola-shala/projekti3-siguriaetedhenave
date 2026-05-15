import socket
import threading
import jwt
from datetime import datetime, timedelta, UTC
from cryptography.hazmat.primitives import serialization

try:
with open("private_key.pem", "rb") as f:
PRIVATE_KEY = serialization.load_pem_private_key(f.read(), password = None)

with open("public_key.pem", "rb") as f:
PUBLIC_KEY = f.read()
except FileNotFoundError:
print("[ERROR] Celesat nuk u gjeten! Ekzekuto 'pygenerate_keys.py' se pari.")
exit()

def handle_client(conn, addr):
print(f"[SERVER] Lidhje e re nga {addr}")
try:
data = conn.recv(1024).decode()
if not data or ":" not in data:
return

username, password = data.split(":")

if USERS.get(username) == password:
payload = {
"sub": username,
"iat": datetime.now(UTC),
"exp": datetime.now(UTC) + timedelta(minutes=30)
}
token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
conn.send(f"SUCCESS:{token}".encode())
print(f"[SERVER] JWT u leshua me sukses per {username}")
else:
conn.send("FAIL: Kredencial te gabuara".encode())
print(f"[SERVER] Deshtim ne login per {username}")
return
