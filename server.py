



        while True:
            request = conn.recv(1024).decode()
            if not request:
                  break
            
            if request.startswith("request_data:"):
                  recieved_token = request.split(":")[1]
                  try:
                        jwt.decode(recieved_token, PUBLIC_KEY, algorithms = ["RS256"])
                        response = '{"data": "Ky eshte nje resurs i mrbojtur nga serveri FIEK."}'
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
        print(f"[SERVER] Gabim gjate ekzekutimit: {e}")
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
            client_thread = threading.Thread(target = handle_client, args = (conn, addr))
            client_thread.start()

if __name__ == "__main__":
      start_server()