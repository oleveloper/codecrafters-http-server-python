import socket

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    client_socket, address = server_socket.accept()
    data = client_socket.recv(1024)
    path = str(data).split("\r\n")[0].split(' ')[1]

    if path == '/': 
      client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    elif path.startswith("/echo/"):
      client_socket.sendall(response(path.replace("/echo/", "")).encode()) 
    else:
      client_socket.sendall(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")

def response(text):
    status_line = "HTTP/1.1 200 OK"
    content_type = "Content-Type: text/plain"
    content_length = f"Content-Length: {len(text)}"
    return f"{status_line}\r\n{content_type}\r\n{content_length}\r\n\r\n{text}"

if __name__ == "__main__":
    main()
