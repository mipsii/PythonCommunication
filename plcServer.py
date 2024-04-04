import pickle
import socket
import subprocess
import sys
from plc import PLC
import time
import asyncio

class ServerPLC():
    def __init__(self, host, port):
        
        self.host = host
        self.port = port
        
        self.client_ids = {} 
        
    def connect_to_client(self):
        pass
    
    def generate_client_id(self, client_type):
        
        if (client_type == "Monitoring"):
            return 2
        if (client_type == "PLC"):
            return 1
        
    async def handle_client(self, reader, writer):
        client_address = writer.get_extra_info('peername')
        print(client_address)
        client_type = (await reader.read(1024))
        client_type = client_type.decode()
        if client_address not in self.client_ids:
            self.client_ids[client_address] = client_type
            print(f"Povezan sa klijentom {client_address}.")
            print(client_type)
        
        try:
            while True:
                client_type = await reader.read(1024)
                await writer.drain()                               
                # Ovde dodajte logiku za slanje podataka klijentu                
                await asyncio.sleep(1)  # Simulacija slanja podataka svake sekunde
                
        except asyncio.CancelledError:
            print(f"Klijent {client_address} je prekinuo konekciju.")
            del self.client_ids[client_address]
            writer.close()
        
    async def start(self):
        """  # Pokretanje PLC 
            subprocess.Popen(['python', 'plc.py'])

            # Pokretanje ServerPLC 
            subprocess.Popen(['python', 'plcServer.py']) """
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"Server je pokrenut na {self.host}:{self.port}")

        #     try:
        #         client_type = client_socket.recv(1024).decode()
        #         client_id = self.generate_client_id(client_type)
        #         print(f"Povezan sa {client_address} ID = {client_id}")
        #         client_socket.sendall(f"Monitoring ID = {client_id}".encode())
        #         # Obrada zahteva od klijenta
        #         """print("radi")
        #         sensor_data = PLC.self.sensors
        #         print(sensor_data)
        #         if sensor_data is not None:
        #             print("salje")
        #             data_to_send = pickle.dumps(sensor_data)
        #             client_socket.sendall(data_to_send)
        #             client_socket.close()
        #         else:
        #             print("nema podataka")
        #             client_socket.close() """
        #     except socket.timeout:
        #         print("Nema konektovanog klijenta.")
        #     except KeyboardInterrupt:
        #         break
        try:
            await server.serve_forever()
        except KeyboardInterrupt:
            server.close()
            await server.wait_closed()

# Inicijalizacija servera
HOST = '127.0.0.1' 
PORT = 12345  
server = ServerPLC(HOST, PORT)
try:
    asyncio.run(server.start())
except KeyboardInterrupt:
    server.stop_server()
    sys.exit(0)
    server.stop()
