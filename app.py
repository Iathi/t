import socket

# Configuração do servidor
HOST = '0.0.0.0'  # Escuta em todas as interfaces
PORT = 5000       # Porta que será escutada

# Criação do socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  # Aceita uma conexão por vez

print(f"[+] Escutando em {HOST}:{PORT}...")

try:
    conn, addr = server_socket.accept()
    print(f"[+] Conexão recebida de {addr[0]}:{addr[1]}")

    # Loop para comunicação
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"[>] Cliente disse: {data.decode().strip()}")
        conn.sendall(b"Mensagem recebida\n")  # Resposta simples

    conn.close()
    print("[*] Conexão encerrada.")

except KeyboardInterrupt:
    print("\n[!] Encerrando servidor...")
finally:
    server_socket.close()

