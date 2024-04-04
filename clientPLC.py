import socket
import pickle
import time
import asyncio

class ClientPLC:

    def __init__(self, host, port, IdMessage):
        self.host = host
        self.port = port
        self.socket = None
        self.IdMessage = IdMessage

    async def send_message(self, message):
        self.socket.sendall(("{self.IdMessage}:"+message).encode())
        print("Poruka poslata:", message)

    async def receive_message(self):
        try:
            response = self.socket.recv(1024)
            return response.decode()
        except ConnectionResetError:
            print("Veza prekinuta sa serverom")
            return None

    def check_server_availability(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.socket.close()
            return True
        except ConnectionRefusedError:
            time.sleep(5)
            return False

    def connect_to_server(self):
        while True:
            if self.check_server_availability():
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                self.send_message(self.IdMessage)
                response = self.receive_message()
                print("Odgovor od servera:", response)
                print("Povezan na server")
                return True
            else:
                print("Nije moguće povezati se na server.")
                time.sleep(5)
                
    async def start(self):
        if self.connect_to_server():  
            while True:         
                    response = self.receive_message()
                    if response is not None:
                        print("Odgovor od servera:", response)
                    self.socket.close()

def main():
    # Adresa i port servera
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 12345

    # Inicijalizacija klijenta
    IdMessage = "Monitoring"
    client = ClientPLC(SERVER_HOST, SERVER_PORT, IdMessage)
    
    # Pokretanje klijenta
    asyncio.run(client.start())

if __name__ == "__main__":
    main()
