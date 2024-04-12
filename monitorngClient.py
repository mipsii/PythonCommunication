import asyncio
from client import Client

class Monitoring:
    def __init__(self, num_sensors, host,port, idMessage):
        self.host = host
        self.port = port
        self.idMessage = idMessage
        self.client = Client(self.host, self.port, self.idMessage)
        self.numSensor = num_sensors
        
    async def start(self):
        while True:    
            await self.client.connect_to_server()
            while True:         
                try:
                    # message = input("Unesite poruku (ili 'quit' za izlaz): ")
                    # if message.lower() == 'quit':
                    #     await self.close_connection()
                    #     return
                                        
                    receive_task = asyncio.create_task(self.client.receive_message())
                    #sending_task = asyncio.create_task(self.client.send_message('   '))
                    await receive_task
                             
                except KeyboardInterrupt:
                    await self.client.close_connection()
                    return
                except ConnectionError:
                    await self.client.close_connection()
                    await asyncio.sleep(1)  # Sačekaj malo pre ponovnog pokušaja povezivanja
                    break
                    
if __name__ == "__main__":
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 12345

    IdMessage = "monitoring"
    monitor = Monitoring(16, SERVER_HOST,SERVER_PORT, IdMessage)
    
    asyncio.run(monitor.start())
    
