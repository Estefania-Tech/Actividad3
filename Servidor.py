
import socket
import threading 

Lista_usuarios = []
Lista_contrasena = []


def login(conn):
    # Proceso de login
    conn.send("Ingrese su nombre de usuario: ".encode('utf-8'))
    username = conn.recv(1024).decode('utf-8')

    conn.send("Ingrese su contraseña: ".encode('utf-8'))
    password = conn.recv(1024).decode('utf-8')
        
    # Validar información
     # Verificar si el nombre de usuario está en la lista
    if username in Lista_usuarios:
        # Obtener el índice del usuario
        index = Lista_usuarios.index(username)
        # Verificar la contraseña usando el índice
        if Lista_contrasena[index] == password:
            conn.send("Login exitoso. Bienvenido a la biblioteca!\n".encode('utf-8'))
            Biblioteca(conn)
        else:
            conn.send("Credenciales incorrectas. La contraseña no coincide.\n".encode('utf-8'))
    else:
        conn.send("El usuario no existe. Favor resgistrarse\n".encode('utf-8'))

def Registrarse(conn):
    conn.send("Ingrese el nombre de usuario: ".encode('utf-8'))
    nombre = conn.recv(1024).decode('utf-8')
    conn.send("Digite la contraseña: ".encode('utf-8'))
    contrasena = conn.recv(1024).decode('utf-8')

    # Almacenar el nuevo usuario y contraseña
    Lista_usuarios.append(nombre)
    Lista_contrasena.append(contrasena)

    # Confirmación al cliente
    conn.send(f"El usuario {nombre} se registró exitosamente.\n".encode('utf-8'))

def Biblioteca(conn):
    Lista_Libros = ["Romeo y Julieta de William S.", "Cien Años de soledad de Gabriel G.M ", "Un mundo feliz de Aldoux H." ]
    conn.send("\n Gracias por visitar la biblioteca! \n Libros disponibles \n".encode('utf-8'))
    for libro in Lista_Libros:
        conn.send(f"- {libro}\n".encode('utf-8'))  
        #la f antes de las comillas indica que 
        #se esta utilizando un f-string o cadena de formato en python 3.6 y son una forma de 
        #formatear cadenas de texto, permitiendo incrustrar expresiones dentro de cadenas 
        #de manera más legibles y concisa
    conn.send("Fin de la lista\n".encode('utf-8'))

def manejar_cliente(conn, addr):
    print("Conexión establecida con {addr}")
    
    while True:
        # Enviar menú al cliente
        menu = """
        ¿Qué desea hacer?
        1. Registrarse
        2. Iniciar sesión
        3. Salir
        """
        conn.send(menu.encode('utf-8'))

        # Recibir opción del cliente
        opcion = conn.recv(1024).decode('utf-8')

        if opcion == "1":
            Registrarse(conn)
        elif opcion == "2":
            login(conn)
        elif opcion == "3":
            conn.send("Hasta luego...".encode('utf-8'))
            break
        else:
            conn.send("Opción inválida. Intente nuevamente.\n".encode('utf-8'))
    conn.close()

def iniciar_servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)
    print("Servidor escuchando en el puerto 8080...")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target= manejar_cliente, args=(conn, addr)).start()
if __name__ == "__main__":
    iniciar_servidor()