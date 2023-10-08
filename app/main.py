import socket

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    client_socket, address = server_socket.accept()
    data = client_socket.recv(1024)
    path = str(data).split("\r\n")[0].split(' ')[1]

    if path == '/': 
      client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    else:
      client_socket.sendall(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")

if __name__ == "__main__":
    main()
