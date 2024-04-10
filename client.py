import asyncio

class Client:
    def __init__(self, host, port, idMessage):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.IdMessage = idMessage

    async def send_message(self, message):
        try:        
            print(f"Poslata poruka: {message}")
            self.writer.write((self.IdMessage+":"+message).encode("utf-8")+ b"\n")
            await self.writer.drain()
            # response = await self.receive_message()
            # print("Primljen odgovor od servera:", response)
            
        except Exception as e:
            print(f"Greška pri slanju poruke: {e}")

    async def receive_message(self):
        print("stigla poruka")
        try:
            data = await self.reader.readline()  
            message = data.decode("utf-8").rstrip() # Uklanjanje zadnjeg bajta (dvotačke) i dekodiranje poruke
            if message:
                print(f"Primljen odgovor: {message}")
                message = message.decode("utf-8").rstrip()
                #sender_id, content = message.split(':', 1)
                
        except Exception as e:
            print(f"Greška pri primanju poruke: {e}")
                
    async def connect(self):
           while True:
            try:
                # Pokušajte da se povežete na server
                print(f"Pokušavam povezivanje na {self.host}:{self.port}")
                self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
                idMessage = self.IdMessage  # Postavite ovo na odgovarajuće ime klijenta
                self.writer.write(f"{idMessage} \n".encode())
                await self.writer.drain()
                print("Uspešno povezan na server!")
                return  # Ako je povezan, prekinite petlju i nastavite sa izvršavanjem programa
            except ConnectionRefusedError:
                print("Server nije dostupan. Čekam 5 sekundi pa ću ponovo pokušati.")
                await asyncio.sleep(5)  # Sačekajte 5 sekundi pre nego što pokušate ponovo
                
    async def close_connection(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
        
    async def start(self):
        while True:    
            await self.connect()
            while True:         
                try:
                    # message = input("Unesite poruku (ili 'quit' za izlaz): ")
                    # if message.lower() == 'quit':
                    #     await self.close_connection()
                    #     return
                                        
                    receive_task = asyncio.create_task(self.receive_message())
           
                    await receive_task
                    self.send_message("reci mo")               
                except KeyboardInterrupt:
                    await self.close_connection()
                    return
                    