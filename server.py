import socket 

s_socket = socket.socket()
#Establecer la conexión 
s_socket.bind(('localhost', 8000))
#Definir cuantas conexiones pueden estar en cola 
s_socket.listen(5)

while True: 
    conexion, addr = s_socket.accept()
    print ("Nueva conexión establecida addr ")
    print (addr)
    
    conexion.send("Conexión exitosa")
    conexion.close()
    