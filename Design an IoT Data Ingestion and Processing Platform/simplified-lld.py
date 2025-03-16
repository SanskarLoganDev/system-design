import time
import random
from queue import Queue, Empty
class driverDetails:
    def __init__(self, name=None, driver_id=None):
        self.name = name
        self.id = driver_id

class IoTDevice:
    def __init__(self,sensor_id= None, device_type= None):
        self.sensor_id = sensor_id
        self.device_type = device_type
        
    def generate_data(self):
        timestamp = time.time()
        sensor_value = random.uniform(10,20)
        return {self.sensor_id: {"value": sensor_value, "timestamp": timestamp, "device_type":self.device_type}}
    
class fleetManagementSystem:
    def __init__(self, vehicle_id= None, sensor_id= None):
        self.vehicle_id = vehicle_id
        self.driver_name= driverDetails().name
        self.sensor_id = sensor_id
        self.fleet_data = {self.sensor_id: {"driver_name": self.driver_name, "vehicle_id": self.vehicle_id}}
        
        
    def get_fleet_details(self, sensor_id):
        return self.fleet_data.get(sensor_id)
    
    
class ingestionService:
    def __init__(self):
        self.fleet_management = fleetManagementSystem()
        self.device = IoTDevice()
        self.message_queue = MessageQueueWrapper()
        
    def ingest(self):
        sensor_id = self.device.sensor_id
        fleet_data = self.fleet_management.get_fleet_details(sensor_id)
        iot_data = self.device.generate_data().get(sensor_id, {})
        enriched_message ={
            "sensor_id": sensor_id,
            "sensor_value": iot_data.get("value"),
            "driver": fleet_data.get("driver_name"),
            "vehicle_id": fleet_data.get("vehicle_id"),
            "timestamp": iot_data.get("timestamp")
        }
        print("Ingesting message: ", enriched_message)
        
        self.message_queue.put(enriched_message)
        return self.message_queue
        
class ProcessingEngine:
    def __init__(self):
        self.ingestion_service = ingestionService()
        self.message_queue = self.ingestion_service.ingest()
        self.storage = StorageService()
    
    def processing(self):
        while True:
            message = self.message_queue.get(timeout=2)
            if message is None:
                break  # No more messages available.
            print("Processing message: ", message)
            # Example processing: add a status flag based on sensor_value.
            sensor_value = message.get("sensor_value", 0)
            message["status"] = "normal" if sensor_value < 15 else "alert"
            self.storage.store(message)
        
        return self.storage.query_data()
          
class MessageQueueWrapper:
    def __init__(self):
        self.queue = Queue()

    def put(self, message):
        self.queue.put(message)

    def get(self, timeout=1):
        try:
            return self.queue.get(timeout=timeout)
        except Empty:
            return None
        
# Storage Service (Mock TimeScaleDB)
class StorageService:
    def __init__(self):
        self.data_store = []

    def store(self, data):
        print(f"Storing data: {data}")
        self.data_store.append(data)

    def query_data(self):
        return self.data_store