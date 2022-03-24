# Chat c/ múltiplos clientes e servidores

# Importando os módulos
import socket
import threading
import queue
import sys
import random
import os

# Servidor
def recebe_dados_servidor(socket, pacotesRecebidos):
    while True:
        dado, endereco = socket.recvfrom(1024)
        pacotesRecebidos.put((dado, endereco))

def roda_servidor():
    host = socket.gethostbyname(socket.gethostname())
    porta = 32092
    print(f"IP Servidor: {host} | Porta: {porta}")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, porta))
    clientes = set()
    pacotesRecebidos = queue.Queue()

    print(f"\nServidor rodando...\n")

    threading.Thread(target = recebe_dados_servidor, args=(s,pacotesRecebidos)).start()

    while True:
        while not pacotesRecebidos.empty():
            dado, endereco = pacotesRecebidos.get()
            
            if (endereco not in clientes):
                clientes.add(endereco)
                continue
            
            clientes.add(endereco)
            
            dado = dado.decode("utf-8")
            
            if (dado == "QUIT"):
                clientes.remove(endereco)
                continue
            
            print(f"{str(endereco)}: {dado}")

            for cliente in clientes:
                if cliente != endereco:
                    s.sendto(dado.encode("utf-8"), cliente)
    s.close()

# Cliente
def recebe_dados_cliente(sock):
    while True:
        try:
            pacote, endereco = sock.recvfrom(1024)
            print(pacote.decode("utf-8"))
        except:
            pass

def roda_cliente(ip_servidor):
    host = socket.gethostbyname(socket.gethostname())
    porta = random.randint(5000, 10000)
    print(f"IP Cliente: {str(host)} | Porta: {str(porta)}\n")
    servidor = (str(ip_servidor), 32092)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, porta))

    usuario = str(input("Digite o nome do usuário: "))
    while (usuario == ""):
        usuario = str(input("Digite o nome do usuário: "))
    print(f"O nome do usuário é {usuario}!\n")
    s.sendto(usuario.encode("utf-8"), servidor)
    threading.Thread(target = recebe_dados_cliente, args=(s,)).start()
    while True:
        mensagem = input(">> ")
        if (mensagem == "QUIT"):
            break
        mensagem = '['+usuario+']' + ':' + ' ' + mensagem
        s.sendto(mensagem.encode("utf-8"), servidor)
    s.sendto(mensagem.encode("utf-8"), servidor)
    s.close()
    os._exit(1)

if __name__ == "__main__":
    if (len(sys.argv) == 1):
        roda_servidor()
    elif (len(sys.argv) == 2):
        roda_cliente(sys.argv[1])
    else:
        print("Rode o servidor: python clienteServidor.py")
        print("Rode o cliente: python clienteServidor.py <endereco servidor>")
