from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import socket
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# Função para lidar com conexões TCP
def handle_client(conn):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Recebido do cliente: {data.decode()}")
            # Enviar a mensagem para todos os clientes conectados ao WebSocket
            socketio.emit('server_message', {'message': data.decode()})
            conn.sendall(b"Mensagem recebida\n")
    finally:
        conn.close()

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Função que roda o servidor TCP em uma thread separada
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5001))  # A escutar na porta 5001
    server_socket.listen(1)
    print("Servidor TCP escutando na porta 5001...")
    
    while True:
        conn, addr = server_socket.accept()
        print(f"Conexão recebida de {addr}")
        threading.Thread(target=handle_client, args=(conn,)).start()

# Roda o servidor TCP em uma thread separada
def run_tcp_server():
    threading.Thread(target=start_server, daemon=True).start()

# Função para iniciar o Flask e SocketIO
def start_flask():
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    # Inicia o servidor TCP antes de iniciar o Flask
    run_tcp_server()
    # Inicia o Flask e o SocketIO
    start_flask()
