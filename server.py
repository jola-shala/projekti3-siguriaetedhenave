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

USERS = {"jane_doe": "password123", "user_1234": "user1234"}

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
            conn.send("FAIL: Kredenciale te gabuara".encode())
            print(f"[SERVER] Deshtim ne login per {username}")
            return

        while True:
            request = conn.recv(1024).decode()
            if not request: 
                break
            
            if request.startswith("request_data:"):
                received_token = request.split(":")[1]
                try:
                    jwt.decode(received_token, PUBLIC_KEY, algorithms = ["RS256"])
                    response = '{"data": "Ky eshte nje resurs i mbrojtur nga serveri FIEK."}'
                    conn.send(response.encode())
                    print(f"[SERVER] Akses i lejuar per {username}")
                except jwt.ExpiredSignatureError:
                    conn.send("ERROR:401 Tokeni ka skaduar".encode())
                    print(f"[SERVER] Tokeni ka skaduar per {username}")
                except jwt.InvalidTokenError:
                    conn.send("ERROR:401 Token i pavlefshem".encode())
                    print(f"[SERVER] Tentim per akses me token te pavlefshem")
            
            elif request == "logout":
                print(f"[SERVER] Perdoruesi {username} u dekonektua.")
                break

    except Exception as e:
        print(f"[SERVER] Gabim gjate komunikimit: {e}")
    finally:
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 5000))
    server.listen(5)
    print("[SERVER] Serveri u nis ne porten 5000... Duke pritur lidhje...")
    
    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()