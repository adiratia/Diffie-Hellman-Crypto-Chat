from AES import AESCipher
from os import urandom
import socket
from sys import byteorder
import json

def recive_message(sock: socket, addr: str, secret: int) -> None:
    while True:
        try:
            msg = sock.recv(4096)
            msg = AESCipher(msg, str(secret)).decrypt()
            if not msg:
                break
            print(f"\033[96m\r{addr} : {msg}\033[0m")
            print("\n> ", end="")
        except socket.error:
            print("[ ERROR: Could not recive message ]")
            break
        except ValueError:
            break

    print(f"[ Connection with {addr} closed ]\n")
    sock.close()   
    
    

def send_message(sock: socket, secret: int) -> None:
    while True:
        msg = input("> ")
        encrypt_client = AESCipher(msg, str(secret)).encrypt()
        try:
            sock.sendall(encrypt_client.encode("utf-8"))
        except socket.error:
            print("[ ERROR: Could not send message ]")
            break
        
    print(f"[ Connection closed ]\n")
    sock.close()

def randomNumber(size: int) :
    return int.from_bytes(urandom(size), byteorder)

def key_exchange(sock: socket, public: int, private: int) :
    # Create the key to be exchanged
    print("[ Initiating key exchange with client ]")
    sock.sendall("Start".encode("utf-8"))

    print("[ Waiting for client public key ]")
    client_public_key = int(sock.recv(4096).decode("utf-8"))

    print("[ Generating exchange key ]")
    exchange_key = pow(client_public_key, private, public)

    print("[ Sending our public key ]")
    sock.sendall(f"{public}".encode("utf-8"))

    print("[ Waiting for client exchange key ]")
    client_ex_key = int(sock.recv(4096).decode("utf-8"))
    print("[ Recieved the client's exchange key ]")

    print("[ Sending server exchange key ]")
    sock.sendall(f"{exchange_key}".encode("utf-8"))

    print("[ Generating shared secret key ]")
    return pow(client_ex_key, private, public)

def recieve(sock: socket) -> str:
    msg = sock.recv(4096).decode("utf-8")
    return msg

def save_to_db(addr, secret_key: int):
    new = { addr : 
        { "secret_key": secret_key }
    }

    with open("data.json", "r+") as file:
        data = json.load(file)
        data.update(new)
        file.seek(0)
        json.dump(data, file)
