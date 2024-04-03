import pickle
import socket
import subprocess
from plc import PLC

class ServerPLC():
    def __init__(self, host, port):
        
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # Čeka na najviše 5 konekcija
        
    def connect_to_client(self):
        pass
    
    def generate_client_id(self, client_type):
        if (client_type == "Monitoring"):
            return 2
        if (client_type == "PLC"):
            return 1
    
    def start(self):
        """  # Pokretanje PLC servera u jednoj konzoli
            subprocess.Popen(['python', 'plc.py'])

            # Pokretanje ServerPLC servera u drugoj konzoli
            subprocess.Popen(['python', 'plcServer.py']) """
                
        print(f"Server je pokrenut na {self.host}:{self.port}")
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                client_type = client_socket.recv(1024).decode()
                client_id = self.generate_client_id(client_type)
                print(f"Povezan sa {client_address} ID = {client_id}")
                client_socket.sendall(f"Monitoring ID = {client_id}".encode())
                # Obrada zahteva od klijenta
                """print("radi")
                sensor_data = PLC.self.sensors
                print(sensor_data)
                if sensor_data is not None:
                    print("salje")
                    data_to_send = pickle.dumps(sensor_data)
                    client_socket.sendall(data_to_send)
                    client_socket.close()
                else:
                    print("nema podataka")
                    client_socket.close() """
            except socket.timeout:
                print("Nema konektovanog klijenta.")
            except KeyboardInterrupt:
                break

    def stop(self):
        self.server_socket.close()
        print("Server je zaustavljen.")

# Inicijalizacija servera
HOST = '127.0.0.1'  # Adresa servera
PORT = 12345  # TCP port
server = ServerPLC(HOST, PORT)
try:
    server.start()
except KeyboardInterrupt:
    server.stop()
