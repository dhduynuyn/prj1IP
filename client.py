import socket
import threading
import json
import os
import shlex

CHUNK_SIZE = 1024 * 1024
CLIENT_FOLDER = "Client"
SERVER_PORT = 12000
SERVER = socket.gethostbyname(socket.gethostname())
SERVER_ADDR = (SERVER, SERVER_PORT)

def multithreaded_download(filenames, progress_callback=None):
    threads = []
    # create thread for each file
    for filename in filenames:
        t = threading.Thread(target=download_file, args=(filename,progress_callback))
        t.start()
        threads.append(t)

    # wait for all threads to finish
    for t in threads:
        t.join()

def download_file(filename, progress_callback=None):
    try:
        # connect server and send GET request
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(SERVER_ADDR)
        sock.send(f"GET {filename}".encode())

        # check file existence in server
        response = sock.recv(1024).decode()
        if response.startswith("ERROR"):
            print(f"[ERROR] {filename}: {response}")
            sock.close()
            return

        # create file
        filesize = int(response)
        filepath = os.path.join(CLIENT_FOLDER, os.path.basename(filename))
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # download file
        with open(filepath, "wb") as f:
            received = 0
            while received < filesize:
                chunk = sock.recv(CHUNK_SIZE)
                if not chunk:
                    break
                f.write(chunk)
                received += len(chunk)
                if progress_callback:
                    progress_callback(received / filesize)

        # print success message
        print(f"[OK] Downloaded {filename} ({filesize} bytes)")
        return True, filepath
    except Exception as e:
        print(f"[EXCEPTION] {filename}: {e}")
        return False, str(e)
    finally:
        sock.close()
    
def list_files():
    # connect to server and send LIST request
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(SERVER_ADDR)
    sock.send("LIST".encode())
    
    # get directory tree from server
    data = b''
    while chunk := sock.recv(4096):
        if not chunk or chunk.decode() == '<END>':
            break
        data += chunk
    
    files = json.loads(data.decode())
    sock.close()
    return files

def main():
    os.makedirs(CLIENT_FOLDER, exist_ok=True)
        
    while True:
        command = input("Enter command (LIST, GET <file1> <file2> ..., QUIT): ").strip()

        # LIST
        if command.upper() == "LIST":
            files = list_files()
            print("Files on server:")
            print(json.dumps(files, indent=2))

        # GET <file1> <file2> ...
        elif command.upper().startswith("GET"):
            parts = shlex.split(command)
            filenames = parts[1:]
            multithreaded_download(filenames)
  
        # QUIT
        elif command.upper() == "QUIT":
            print("Disconnected.")
            break

if __name__ == "__main__":
    main()
