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
                self.writer.write((message).encode("utf-8")+ b"\n")
                await self.writer.drain()
                # response = await self.receive_message()
                # print("Primljen odgovor od servera:", response)
            # else:
            #     print("Ne postoji server")
            #     self.connect_to_server()
            
        except Exception as e:
            print(f"Greška pri slanju poruke: {e}")

    # async def send_ping(self):
    #     self.writer.write("ping".encode())
    #     await self.writer.drain()

    #     data = await self.reader.readline()
    #     response = data.decode("utf-8")
    #     if response=="pong":
    #         return True
    #     else:
    #         return False
        
       
    async def receive_message(self):
        #print("stigla poruka")
        server_unavailable_message_printed = False  # Promenljiva koja prati da li je već ispisana poruka o nedostupnosti servera

        try:
            data = await self.reader.readline()  
            message = data.decode("utf-8").rstrip()
            if message:
                print(f"Primljen odgovor: {message}")
                server_unavailable_message_printed = False
                
            else:
                server_unavailable_message_printed=True
                print("server nije dostupan")
                await self.connect_to_server()
                #message = message.decode("utf-8").rstrip()
                #sender_id, content = message.split(':', 1)
                
        except Exception as e:
            print(f"Greška pri primanju poruke: {e}")
            
            #server_unavailable_message_printed = True
                
    async def connect(self):
           while True:
            try:
                # Pokušajte da se povežete na server
                print(f"Pokušavam povezivanje na {self.host}:{self.port}")
                self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
                idMessage = self.IdMessage  # Postavite ovo na odgovarajuće ime klijenta
                self.writer.write(f"{self.IdMessage} \n".encode())
                await self.writer.drain()
                print("Uspešno povezan na server!", self.IdMessage)
                return  # Ako je povezan, prekinite petlju i nastavite sa izvršavanjem programa
            except ConnectionRefusedError:
                print("Server nije dostupan. Čekam 5 sekundi pa ću ponovo pokušati.")
                await asyncio.sleep(5)  # Sačekajte 5 sekundi pre nego što pokušate ponovo
                
    async def close_connection(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
    
    async def connect_to_server(self):
        try:
            # Pokušajte da se povežete sa serverom sa vremenskim ograničenjem od 5 sekundi
            await self.connect()
            print("Uspešno povezan sa serverom.")
            return
        except asyncio.TimeoutError:
            print("Nije moguće povezati se sa serverom u roku od 5 sekundi.")
            await asyncio.sleep(1)
            
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
                    