import time
import random
from queue import Queue, Empty

# Simulated Fleet Management Database (Mock DB)
class FleetManagement:
    def __init__(self):
        # Mock database mapping sensor_id to vehicle and driver
        self.fleet_data = {
            "tempSensor-001": {"fleet_vehicle_number": "Fleet-1234", "current_driver": "John Doe"},
            "tempSensor-002": {"fleet_vehicle_number": "Fleet-5678", "current_driver": "Alice Smith"},
            "tempSensor-003": {"fleet_vehicle_number": "Fleet-9012", "current_driver": "Bob Williams"},
        }

    def get_fleet_info(self, sensor_id):
        """ Fetch fleet vehicle and driver info for a given sensor ID """
        return self.fleet_data.get(sensor_id, {"fleet_vehicle_number": "Unknown", "current_driver": "Unknown"})

# IoT Device Class (Simulating Sensors)
class Device:
    def __init__(self, device_id, device_type):
        self.device_id = device_id
        self.device_type = device_type

    def generate_data(self):
        """ Generate sensor data with a random temperature reading """
        sensor_value = random.uniform(20.0, 30.0)  # Simulated temperature
        timestamp = time.time()
        return Message(self.device_id, sensor_value, timestamp)

# Sensor Data Message Class
class Message:
    def __init__(self, device_id, sensor_value, timestamp):
        self.device_id = device_id
        self.sensor_value = sensor_value
        self.timestamp = timestamp

    def __str__(self):
        return f"Message(device_id={self.device_id}, sensor_value={self.sensor_value:.2f}, timestamp={self.timestamp})"

# Message Queue (Acts as a buffer between ingestion and processing)
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

# Ingestion Service (Handles validation and enrichment)
class IngestionService:
    def __init__(self, message_queue, fleet_management):
        self.message_queue = message_queue
        self.fleet_management = fleet_management

    def ingest(self, message):
        """ Validate, enrich, and enqueue sensor data """
        if message.sensor_value is None or message.timestamp is None:
            print("Invalid message received.")
            return False

        # Fetch fleet info
        fleet_info = self.fleet_management.get_fleet_info(message.device_id)

        # Enrich message with fleet details
        enriched_message = {
            "sensor_id": message.device_id,
            "sensor_value": message.sensor_value,
            "timestamp": message.timestamp,
            "fleet_vehicle_number": fleet_info["fleet_vehicle_number"],
            "current_driver": fleet_info["current_driver"]
        }

        print(f"Ingesting: {enriched_message}")

        # Send to local queue for processing
        self.message_queue.put(enriched_message)
        return True

# Processing Engine (Consumes and processes messages)
class ProcessingEngine:
    def __init__(self, message_queue, storage_service):
        self.message_queue = message_queue
        self.storage_service = storage_service

    def process_messages(self):
        """ Process messages from the queue """
        while True:
            message = self.message_queue.get(timeout=2)
            if message is None:
                break  # No messages to process

            print(f"Processing: {message}")

            # Simulated data transformation
            enriched_data = {
                **message,  # Retain all existing fields
                "status": "normal" if message["sensor_value"] < 25 else "alert"
            }

            # Store in TimeScaleDB (mocked)
            self.storage_service.store(enriched_data)

# Storage Service (Mock TimeScaleDB)
class StorageService:
    def __init__(self):
        self.data_store = []

    def store(self, data):
        print(f"Storing data: {data}")
        self.data_store.append(data)

    def query_data(self):
        return self.data_store

# Running the System (Simulated Fleet IoT Data Pipeline)
if __name__ == "__main__":
    # Initialize system components
    fleet_management = FleetManagement()
    message_queue = MessageQueueWrapper()
    storage_service = StorageService()
    ingestion_service = IngestionService(message_queue, fleet_management)
    processing_engine = ProcessingEngine(message_queue, storage_service)

    # Create fleet sensor devices
    devices = [
        Device(device_id="tempSensor-001", device_type="TemperatureSensor"),
        Device(device_id="tempSensor-002", device_type="TemperatureSensor"),
        Device(device_id="tempSensor-003", device_type="TemperatureSensor")
    ]

    # Simulating data collection and processing
    for round_num in range(3):  # Simulate 3 rounds of data collection
        print(f"\n--- Data Generation Round {round_num + 1} ---")
        for device in devices:
            msg = device.generate_data()
            ingestion_service.ingest(msg)

        # Process messages (simulating background processing)
        processing_engine.process_messages()

    # Display stored data
    stored_data = storage_service.query_data()
    print("\nFinal stored data in TimeScaleDB:")
    for data in stored_data:
        print(data)
