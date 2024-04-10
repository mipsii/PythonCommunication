import asyncio
import random
import time
from client import Client

class PLC:
    def __init__(self, num_sensors, host,port, idMessage):
        self.num_sensors = num_sensors
        self.sensor_register = None  #  svi senzori su isključeni
        self.previous_states = None
        self.host = host
        self.port = port
        self.socket = None
        self.idMessage = idMessage
        self.client = Client(self.host, self.port, self.idMessage)

    def read_sensors(self):
        # Simulacija  stanja senzora
        self.sensor_register = random.randint(0, 2**self.num_sensors - 1)

    
    def detect_change_all(self):
        if (self.sensor_register != self.previous_states):
            self.bin_sensor_register = bin(self.sensor_register)[2:].zfill(self.num_sensors)
            self.previous_states = self.sensor_register
            return self.bin_sensor_register
        else:
            return None     
    def detect_changes(self):
        # Detekcija promena stanja senzora        
        # for i in range(self.num_sensors):
        #     current_state = (self.sensor_register >> i) & 1
        #     previous_state = (self.previous_states >> i) & 1
        #     if current_state != previous_state:
        #         print(self.num_sensors)
        #         print(f"Senzor {i+1}: Promena stanja -> {current_state}")
        self.previous_states = self.sensor_register  # Ažuriranje prethodnog stanja senzora
            
    def print_sensor_register(self):
        # Prikaz stanja senzora u binarnom formatu
        self.bin_sensor_register = bin(self.sensor_register)[2:].zfill(self.num_sensors)
        print(self.bin_sensor_register)  # Konvertovanje u binarni format sa 16 bita
        return self.bin_sensor_register
    
    async def connect_to_server(self):
        try:
            # Pokušajte da se povežete sa serverom sa vremenskim ograničenjem od 5 sekundi
            await self.client.connect()
            print("Uspešno povezan sa serverom.")
            return
        except asyncio.TimeoutError:
            print("Nije moguće povezati se sa serverom u roku od 5 sekundi.")
            await asyncio.sleep(5)
            
    async def send_data_to_server(self):
        try:        
            if self.client.writer and not self.client.writer.is_closing():
                print("Server je dostupan, šaljem poruku")
                await self.client.send_message(self.sensors)
            else:
                print("------Server nije dostupan \n")              
        except ConnectionError:
            print("Veza sa serverom je prekinuta. Ne mogu poslati poruku.")
            
    async def read_sensors_task(self):
        while True:                  
                try:
                    self.sensors = self.detect_change_all()
                    print("----------------------")
                    print("Senzori:", self.sensors)                 
                    if (self.sensors):
                        print("DO SERVERa")
                        await self.send_data_to_server()             
                    self.read_sensors() # Simulacija čitanja senzora 
                    #print("provera",self.print_sensor_register())        
                    print("----------------------")
                    await asyncio.sleep(random.randint(1,10))  # obrade podataka svake sekunde
                except KeyboardInterrupt:
                    break   
                except ConnectionError:
                    print("Veza sa serverom je prekinuta. Prestajem slati podatke.")
                    break 
                
    async def run(self):
        while True:    
            #self.client.idRecieve = "clientPlcE"
            try:
                # Pokretanje procesa povezivanja sa serverom i čitanja senzora paralelno
                await asyncio.gather(self.connect_to_server(), self.read_sensors_task())
                print("izasao iz petlje")
            except KeyboardInterrupt:
                break               
            
if __name__ == "__main__":
    # PLC sa 16 senzora
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 12345

    IdMessage = "plc"
    plc = PLC(16, SERVER_HOST,SERVER_PORT, IdMessage)
    
    asyncio.run(plc.run())