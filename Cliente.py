
import socket

def iniciar_cliente():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    while True:
        # Recibe mensaje del servidor
        mensaje = client_socket.recv(1024).decode('utf-8')
        print(mensaje, end='')  # end='' para evitar un salto de línea extra

        # Enviar respuesta (nombre de usuario o contraseña)
        respuesta = input()
        client_socket.send(respuesta.encode('utf-8'))

        if "Login exitoso" in mensaje:
            break  # Salir del bucle si el login fue exitoso

    while True:
        respuesta = client_socket.recv(1024).decode('utf-8')
        if not respuesta:
            break
        print(respuesta, end='')

    client_socket.close()

if __name__ == "__main__":
    iniciar_cliente()




