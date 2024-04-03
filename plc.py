import random
import time
from clientPLC import ClientPLC

class PLC:
    def __init__(self, num_sensors, host,port, IdMessage):
        self.num_sensors = num_sensors
        self.sensor_register = 0  #  svi senzori su isključeni
        self.previous_states = 0
        self.host = host
        self.port = port
        self.socket = None
        self.IdMessage = IdMessage

    def read_sensors(self):
        # Simulacija  stanja senzora
        self.sensor_register = random.randint(0, 2**self.num_sensors - 1)

    
    def detect_change_all(self):
        if (self.sensor_register & self.previous_states):
            return self.print_sensor_register()
        else:
            return None     
    # @property
    # def sensors(self):
    #     # Vratiti podatke o senzorima
    #     return self._sensors
    
    # @sensors.setter
    # def sensors(self, value):
    #     self._sensors = value
        
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

    def run(self):
        while True:
            
            try:
                self.sensors = self.detect_change_all()
                print(self.sensors)
                self.read_sensors()
                self.detect_changes()
                time.sleep(random.randint(1,10))  # Simulacija čitanja senzora i obrade podataka svake sekunde
            except KeyboardInterrupt:
                break    
            
if __name__ == "__main__":
    # PLC sa 16 senzora
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 12345

    IdMessage = "PLC"
    plc = PLC(16, SERVER_HOST,SERVER_PORT, IdMessage)
    
    plc.run()