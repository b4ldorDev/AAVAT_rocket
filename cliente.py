import socket

s_socket = socket.socket()
s_socket.connect(('localhost', 8000))

s_socket.send("Hola desde el cliente")
#El 1024 hace referencia al buffer 1024 byte
respuesta = s_socket.recv (1024)
print(respuesta)
s_socket.close()
