from handler import *
from socket import socket, gethostname, AF_INET, SOCK_STREAM
from _thread import start_new_thread

PORT = 8080
IP = '127.0.0.1'

if __name__ == "__main__":
    s = socket(AF_INET, SOCK_STREAM)
        
    # Generate all the keys used for encryption
    public_key = randomNumber(32)
    private_key = randomNumber(32)

    print(f"[ Connecting to {IP}:{PORT} ]")
    s.connect((IP, PORT))
    print("[ Connected to Server ]")
    
    print("[ Waiting for key exchange to be initiated ]")

    while True:
        msg = s.recv(4096).decode("utf-8")

        if msg == "Start":
            print("[ Key exchange started ]")

            print("[ Sending public key ]")
            s.sendall(f"{public_key}".encode("utf-8"))

            print("[ Receiving server public key ]")
            server_public_key = int(s.recv(4096).decode("utf-8"))

            print("[ Generating exchange key ]")
            ex_key = pow(public_key, private_key, server_public_key)

            print("[ Sending exchange key ]")
            s.sendall(f"{ex_key}".encode("utf-8"))

            print("[ Waiting for server key ]")
            server_key = int(s.recv(4096).decode("utf-8"))
            print("[ Received server key ]")

            print("[ Generating secret key ]")
            SECRET_KEY = pow(server_key, private_key, server_public_key)

            save_to_db(IP, SECRET_KEY)

            break
    
    print("The chat is open for sending messages: ")

    start_new_thread(recive_message, (s, gethostname(), SECRET_KEY))

    send_message(s, SECRET_KEY)
