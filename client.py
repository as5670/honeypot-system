import socket

HOST = "127.0.0.1"
PORT = 2222


def receive_response(sock):
    """Receive data from server until no more arrives."""
    response = b""
    sock.settimeout(2.0)
    try:
        while True:
            chunk = sock.recv(1024)
            if not chunk:
                break
            response += chunk
            # Stop reading once we get a prompt ending with ": " or "\r\n"
            if response.endswith(b": ") or response.endswith(b"\r\n"):
                break
    except socket.timeout:
        pass
    return response.decode(errors="replace")


def connect(username, password):
    print(f"[*] Connecting to {HOST}:{PORT}...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"[+] Connected.")

            # Receive banner (e.g. SSH-2.0-OpenSSH_7.4)
            banner = receive_response(s)
            print(f"[SERVER] {banner.strip()}")

            # Receive "Username: " prompt and send username
            prompt = receive_response(s)
            print(f"[SERVER] {prompt.strip()}")
            s.send((username + "\n").encode())

            # Receive "Password: " prompt and send password
            prompt = receive_response(s)
            print(f"[SERVER] {prompt.strip()}")
            s.send((password + "\n").encode())

            # Receive final response (e.g. "Login failed")
            result = receive_response(s)
            print(f"[SERVER] {result.strip()}")

    except ConnectionRefusedError:
        print(f"[!] Connection refused. Is the server running on port {PORT}?")
    except Exception as e:
        print(f"[!] Error: {e}")


if __name__ == "__main__":
    # Example test credentials
    test_username = input("Enter username to test: ").strip()
    test_password = input("Enter password to test: ").strip()
    connect(test_username, test_password)