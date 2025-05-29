import socket
import threading
import json
import os

CHUNK_SIZE = 1024 * 1024
SERVER_FOLDER = "Server"
SERVER_PORT = 12000
SERVER = socket.gethostbyname(socket.gethostname())
SERVER_ADDR = (SERVER, SERVER_PORT)

def build_directory_tree(path):
    tree = []
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            tree.append({
                "name": item,
                "type": "folder",
                "children": build_directory_tree(full_path)
            })
        else:
            tree.append({
                "name": item,
                "type": "file",
                "size": os.path.getsize(full_path),
                "path": full_path[len(SERVER_FOLDER) + 1:]
            })
    return tree

def transfer_file(conn, filepath):
    if os.path.exists(filepath):
        conn.send(f"{os.path.getsize(filepath)}".encode())
        with open(filepath, "rb") as f:
            while chunk := f.read(CHUNK_SIZE):
                conn.send(chunk)
    else:
        conn.send("ERROR File not found".encode())

def handle_command(conn, addr):
    print(f"[CONNECT] {addr}")

    try:
        while True:
            command = conn.recv(1024).decode()

            if command == "LIST":
                directory_tree = build_directory_tree(SERVER_FOLDER)
                json_data = json.dumps(directory_tree)
                conn.sendall(json_data.encode())
                conn.send("<END>".encode())  

            elif command.startswith("GET"):
                _, filepath = command.split(maxsplit=1)
                filepath = os.path.join(SERVER_FOLDER, filepath)
                transfer_file(conn, filepath)

            elif command == "QUIT" or not command:
                break
    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        conn.close()
        print(f"[CLOSE] {addr}")

def start_server():
    os.makedirs(SERVER_FOLDER, exist_ok=True)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(SERVER_ADDR)
    server.listen()
    print(f"[START] Server running on {SERVER}:{SERVER_PORT}")
    
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_command, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
