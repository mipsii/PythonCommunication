import logging
import pickle
import socket
import subprocess
import sys
import time
import asyncio
import queue
class ServerPLC():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_ids = {} 
        self.message_queue = asyncio.Queue()

    async def handle_client(self, reader, writer):
        
        client_address = writer.get_extra_info('peername')
        print(f"test  {client_address} ")
        if client_address not in self.client_ids:
            idName = await reader.readline()      
            idName = idName.decode("utf-8").rstrip()
            print("id Name: ",idName) 
            self.client_ids[idName] = writer
            print(f"Povezan sa klijentom {idName}.")        
        try:            
            while True:              
                client_data = await reader.readline()      
                if not client_data:
                    break
                print("client data",client_data)
                
                client_data = client_data.decode("utf-8").rstrip()
                sender_id, content = client_data.split(':', 1)
        
                message = await self.messageClient(sender_id,content)
                await self.message_queue.put(message)
                print(f"Primljena poruka od klijenta {sender_id}: {content}")
                
                # Ovde dodajte logiku za obradu primljene poruke

                # Potvrda prijema poruke nazad klijentu
                # confirmation_message = "Primljena poruka: " + client_data.decode()
                # print(confirmation_message)
                # writer.write(confirmation_message.encode())
                # await writer.drain()                               
                # Ovde dodajte logiku za slanje podataka klijentu                
                await asyncio.sleep(0.5)  # Simulacija slanja podataka svake sekunde
                
        except asyncio.CancelledError:
            print(f"Klijent {client_address} je prekinuo konekciju.")
            if writer:
                writer.close()
                await writer.wait_closed()
            del self.client_ids[client_address]
            
    async def messageClient(self, idClient, messageServer):
        match idClient:
            case "plcE": idClient="plc"
            case "clientPlcE" : idClient="clientPlc"
        return f"{idClient}:{messageServer}"            
        
    async def start(self):
        """  # Pokretanje PLC 
            subprocess.Popen(['python', 'plc.py'])
            # Pokretanje ServerPLC 
            subprocess.Popen(['python', 'plcServer.py']) """
        # logging.basicConfig(filename='server.log', level=logging.DEBUG)
        # logger = logging.getLogger('server')

       
        try:
            server = await asyncio.start_server(self.handle_client, self.host, self.port)
            print(f"Server je pokrenut na {self.host}:{self.port}")
            async with server:
                while True:
                    if not self.message_queue.empty():
                        await self.send_message_to_client()
                
                    await asyncio.sleep(0.51)  # provera 
                
        except KeyboardInterrupt:
            print("Prekid izvršavanja...")
            server.stop_server()  # Dodajte ovu metodu kako biste ručno zaustavili serve
            
    async def stop_server(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
                          
    async def send_message_to_client(self):
        while True:
            try:
                # Čitanje poruke iz FIFO reda
                message = await self.message_queue.get()

                # Izdvajanje informacije o tome kome je poruka namenjena
                recipient_id, message_content = message.split(':', 1)

                # Pronalaženje odgovarajućeg klijenta na osnovu ID-ja
                writer = self.client_ids.get(recipient_id)
                if writer:
                    # Slanje poruke klijentu
                    writer.write(message_content.encode('utf-8') + b'\n')
                    await writer.drain()
                    print(f"Poruka poslata klijentu sa ID-jem {recipient_id}: {message_content}")
                else:
                    print(f"Klijent sa ID-jem {recipient_id} nije pronađen.")
            except Exception as e:
                print(f"Greška pri obradi poruke iz FIFO reda: {e}")
                
    async def send_message_to_clients(self, message):
        async for writer in self.client_ids.values():
            try:
                print(f"Poslata poruka: {message}")
                
                writer.write(message.encode('utf-8')+ b'\n')  # Slanje poruke kao bajtova
                await writer.drain()
                # response = await self.receive_message()
                # print("Primljen odgovor od servera:", response)
            except Exception as e:
                print(f"Greška pri slanju poruke: {e}")
            except KeyboardInterrupt:
                self.server.close()
                await self.server.wait_closed()  # Sačekaj da se server zatvori
    
async def main():
    # Inicijalizacija servera
    HOST = '127.0.0.1' 
    PORT = 12345  
    server = ServerPLC(HOST, PORT)
    try:        
        await server.start()                
    except KeyboardInterrupt:
        sys.exit(0)
       
        
if __name__ == "__main__":
    asyncio.run(main())
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