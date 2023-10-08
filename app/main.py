import socket

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
      client_socket, address = server_socket.accept()
      data = client_socket.recv(1024)
      prepare_client(data, client_socket)
      client_socket.close()


def prepare_client(data, client_socket):
    lists = str(data).split("\\r\\n")
    path = lists[0].split(' ')[1].strip()
    text = lists[2].split(' ')[1] if path == "/user-agent" else path

    if path == '/': 
      client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    elif path.startswith("/echo/") or path.startswith("/user-agent"):
      text = text.replace("/echo/", "")
      client_socket.sendall(compose_response(text, len(text)).encode()) 
    else:
      client_socket.sendall(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")


def compose_response(text, text_len):
    status_line = "HTTP/1.1 200 OK"
    content_type = "Content-Type: text/plain"
    content_length = f"Content-Length: {text_len}"

    return f"{status_line}\r\n{content_type}\r\n{content_length}\r\n\r\n{text}"

if __name__ == "__main__":
    main()
