from handler import *
from socket import SOL_SOCKET, SO_REUSEADDR, gethostbyname, socket, AF_INET, SOCK_STREAM
from _thread import start_new_thread
import json

PORT = 8080
IP = '127.0.0.1'

def start_server():
    ADDR = (IP, PORT)
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    server_socket.bind(ADDR)
    server_socket.listen(5)

    print(f"[ Server started on {IP}:{PORT} ]")

    return server_socket

if __name__ == "__main__":
    sock = start_server()
    
    with open("data.json", mode='w', encoding='utf-8') as f:
        json.dump({}, f)

    # Generate all the keys used for encryption
    public_key = randomNumber(32)
    private_key = randomNumber(32)
    SECRET_KEY = None
    
    client_socket, client_addr = sock.accept()
    print(f'[ {client_addr} connected ]')
        
    SECRET_KEY = key_exchange(client_socket, public_key, private_key)

    save_to_db("ubuntu", SECRET_KEY)
    
    print(" The chat is open for sending messages: ")

    start_new_thread(recive_message, (client_socket, client_addr, SECRET_KEY))

    send_message(client_socket, SECRET_KEY)
