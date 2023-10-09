import socket
import os
import sys
from threading import Thread

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen()

    while True:
      client_socket, client_address = server_socket.accept()
      Thread(target=prepare_client, args=(client_socket,)).start()


def prepare_client(client_socket):
    data = client_socket.recv(1024).decode()
    lists = str(data).split("\r\n")
    method = lists[0].split(' ')[0]
    path = lists[0].split(' ')[1]
    text = lists[2].split(' ')[1] if path == "/user-agent" else path[path.find('/', 1) + 1:]
    content = bytes(lists[-1], "utf-8") if len(lists) > 5 else ""

    if path == '/': 
      client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n")
    elif path.startswith('/echo/') or path.startswith("/files/") or path.startswith("/user-agent"):
      if len(sys.argv) > 1 and os.path.exists(sys.argv[-1] + text) == False and method != "POST":
        client_socket.send(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")
      else: 
        client_socket.send(compose_response(method, text, content).encode())
    else:
      client_socket.send(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")
    
    client_socket.close()


def compose_response(method, text, content):
    isFile = len(sys.argv) > 1
    if len(sys.argv) > 1:
      file_path = sys.argv[-1] + text
      if method == "POST":
        with open(file_path, "wb") as file: 
           file.write(content)
           file.close()
        return "HTTP/1.1 201 Created\r\n\r\n"
      else: 
        file = open(file_path, "rb")
        text_len = os.path.getsize(file_path)
        text = file.read().decode('utf-8')
        file.close()
    else: 
      text_len = len(text) 

    status_line = "HTTP/1.1 200 OK"
    content_type = "Content-Type: application/octet-stream" if isFile else "Content-Type: text/plain"
    content_length = f"Content-Length: {text_len}"

    return f"{status_line}\r\n{content_type}\r\n{content_length}\r\n\r\n{text}"


if __name__ == "__main__":
    main()
