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
        self.log_file = "message_log.txt"

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
                                
                client_data = client_data.decode("utf-8").rstrip()
                if client_data=="ping":
                    writer.write("pong".encode("utf-8"))
                    await writer.drain()
                else:
                    sender_id, content = client_data.split(':', 1)

                    #message = await self.messageClient(client_data)
                    await self.message_queue.put(client_data)
                    print(f"Primljena poruka od klijenta {sender_id}: {content}")
                    
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
                print("---------------")
                while True:
                    if not self.message_queue.empty():
                        print("fifo nije prazan")
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
            print("------------------")
            try:
                # Čitanje poruke iz FIFO reda
                message = await self.message_queue.get()
                #with open(self.log_file, "a") as f: f.write(f"{message} \n")
            
                # Izdvajanje informacije o tome kome je poruka namenjena
                recipient_id, message_content = message.split(':', 1)

                # Pronalaženje odgovarajućeg klijenta na osnovu ID-ja
                
                if recipient_id in self.client_ids:
                    writer = self.client_ids[recipient_id]
                    # Slanje poruke klijentu
                    writer.write(message_content.encode("utf-8") + b'\n')
                    await writer.drain()
                    print(f"Poruka poslata klijentu sa ID-jem {recipient_id}: {message_content}")
                else:
                    print(f"Klijent sa ID-jem {recipient_id} nije pronađen.")
            except Exception as e:
                print(f"Greška pri obradi poruke iz FIFO reda: {e}")
        
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