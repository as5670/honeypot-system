import socket
import datetime
import hashlib
import time
import threading

HOST = "0.0.0.0"
PORT = 2222


def receive_input(client):
    data = client.recv(1024).decode()
    return data.replace("\r", "").replace("\n", "").strip()


def handle_client(client, addr):
    print(f"[+] Connection from {addr}")
    try:
        client.send(b"SSH-2.0-OpenSSH_7.4\r\n")
        time.sleep(0.5)

        # USERNAME
        client.send(b"Username: ")
        username = receive_input(client)

        # PASSWORD
        client.send(b"Password: ")
        password = receive_input(client)

        print(f"[DEBUG] Username: {username}, Password: {password}")

        # HASH PASSWORD
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        log = f"{datetime.datetime.now()} | {addr[0]} | {username} | {hashed_password}\n"

        with open("logs.txt", "a") as f:
            f.write(log)

        client.send(b"Login failed\r\n")

    except Exception as e:
        print(f"[!] Error handling {addr}: {e}")

    finally:
        client.close()
        print(f"[-] Connection closed: {addr}")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # FIX: Allow reuse of address so server doesn't crash on restart
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(50)

    print(f"🚨 Honeypot running on port {PORT}...")

    try:
        while True:
            client, addr = server.accept()
            # FIX: Handle each client in its own thread so server isn't blocked
            t = threading.Thread(target=handle_client, args=(client, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\n[!] Shutting down honeypot.")
    finally:
        server.close()


if __name__ == "__main__":
    main()
