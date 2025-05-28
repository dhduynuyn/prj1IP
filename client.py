import socket
import threading
import json
import os

CHUNK_SIZE = 1024 * 1024
CLIENT_FOLDER = "Client"
SERVER_PORT = 12000
SERVER = socket.gethostbyname(socket.gethostname())
SERVER_ADDR = (SERVER, SERVER_PORT)

def download_file(filename):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVER_ADDR)
    sock.send(f"GET {filename}".encode())

    response = sock.recv(1024).decode()
    if response.startswith("ERROR"):
        print(f"[ERROR] {filename}: {response}")
        sock.close()
        return

    filesize = int(response)
    full_path = os.path.join(CLIENT_FOLDER, filename)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "wb") as f:
        received = 0
        while received < filesize:
            chunk = sock.recv(CHUNK_SIZE)
            if not chunk:
                break
            f.write(chunk)
            received += len(chunk)

    print(f"[OK] Downloaded {filename} ({filesize} bytes)")
    sock.close()

def main():
    os.makedirs(CLIENT_FOLDER, exist_ok=True)

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(SERVER_ADDR)
        
    while True:
        command = input("Enter command (LIST, GET <file1> <file2> ..., QUIT): ").strip()

        if command == "LIST":
            client_sock.send(command.encode())
            data = client_sock.recv(4096).decode()
            files = json.loads(data)
            print("Files on server:")
            print(json.dumps(files, indent=2))

        elif command.startswith("GET"):
            parts = command.split()
            filenames = parts[1:]

            threads = []
            for filename in filenames:
                t = threading.Thread(target=download_file, args=(filename,))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()
                
        elif command == "QUIT":
            client_sock.send(command.encode())
            print("Disconnected from server.")
            break
        
    client_sock.close()

main()
