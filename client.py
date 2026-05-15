import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('127.0.0.1', 5000))
        
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        client.send(f"{username}:{password}".encode())
        response = client.recv(2048).decode()
        
        if response.startswith("SUCCESS:"):
            token = response.split(":")[1]
            print(f"Logged in. JWT token is: {token}")
            
            while True:
                cmd = input("Enter command ('request_data' or 'logout'): ")
                if cmd == "request_data":
                    client.send(f"request_data:{token}".encode())
                    data = client.recv(1024).decode()
                    print(f"Protected data received: {data}")
                elif cmd == "logout":
                    client.send("logout".encode())
                    print("Logging out...")
                    break
        else:
            print(f"Login failed: {response}")
            
    except Exception as e:
        print(f"Gabim: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()
    