# PROBLEM STATEMENT: Design an IoT Data Ingestion and Processing Platform

# Create a design that gathers vehicle data (like location, speed, engine status) in real time, processes it, and provides actionable insights for fleet management. Think about handling high-frequency data streams and ensuring low-latency analytics.

# Might ask, what kind of data is being asked here (maybe location, speed, engine status)

import time
import random
# We'll start by defining a Device class that simulates an IoT device and a Message class that represents the data payload.

# Question: "For our simulation, can we assume each device sends a temperature reading (a float) along with a timestamp? Or do you want to include any additional information?"

# Device class simulates an IoT device generating sensor data.
class IoTDevice:
    def __init__(self, device_id, device_type):
        self.device_id = device_id
        self.device_type = device_type

    def generate_data(self):
        # Simulate generating sensor data: here we use a temperature value.
        sensor_value = random.uniform(20.0, 30.0)  # Temperature in degrees Celsius
        timestamp = time.time()
        # Create and return a Message object with the generated data.
        return Message(self.device_id, sensor_value, timestamp)

# Message class encapsulates a data payload from a device.
class Message:
    def __init__(self, device_id, sensor_value, timestamp):
        self.device_id = device_id
        self.sensor_value = sensor_value
        self.timestamp = timestamp

    def __str__(self):
        return f"Message(device_id={self.device_id}, sensor_value={self.sensor_value:.2f}, timestamp={self.timestamp})"
    
    
# Follow-Up Question: "Is using an in-memory queue sufficient for this demonstration"


from queue import Queue, Empty

# IngestionService receives messages from devices, validates them, and enqueues them.
class IngestionService:
    def __init__(self, message_queue):
        self.message_queue = message_queue

    def ingest(self, message):
        # Basic validation: ensure sensor_value and timestamp are not None.
        if message.sensor_value is None or message.timestamp is None:
            print("Invalid message received.")
            return False
        # Enqueue the valid message.
        print(f"Ingesting: {message}")
        self.message_queue.put(message)
        return True

# MessageQueueWrapper simulates the buffering layer between ingestion and processing.
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

# ProcessingEngine processes messages from the queue and forwards processed data to storage.
class ProcessingEngine:
    def __init__(self, message_queue, storage_service):
        self.message_queue = message_queue
        self.storage_service = storage_service

    def process_messages(self):
        # Process messages in a loop.
        while True:
            message = self.message_queue.get(timeout=2)
            if message is None:
                # If no message is available, break out of the loop for this demonstration.
                break
            print(f"Processing: {message}")
            # Enrich the message: for example, add a simple quality flag based on the sensor value.
            enriched_data = {
                "device_id": message.device_id,
                "sensor_value": message.sensor_value,
                "timestamp": message.timestamp,
                "status": "normal" if message.sensor_value < 25 else "alert"
            }
            # Forward the enriched data to the storage service.
            self.storage_service.store(enriched_data)

# StorageService simulates persisting processed data.
class StorageService:
    def __init__(self):
        self.data_store = []

    def store(self, data):
        print(f"Storing data: {data}")
        self.data_store.append(data)

    def query_data(self):
        # Return the stored data.
        return self.data_store

# Implementation using main, not generally required

if __name__ == "__main__":
    # Initialize components: message queue, storage, ingestion service, and processing engine.
    message_queue = MessageQueueWrapper()
    storage_service = StorageService()
    ingestion_service = IngestionService(message_queue)
    processing_engine = ProcessingEngine(message_queue, storage_service)

    # Create a list of simulated devices.
    devices = [IoTDevice(device_id=i, device_type="TemperatureSensor") for i in range(1, 6)]

    # Simulate data generation and ingestion in multiple rounds.
    for round_num in range(1, 4):
        print(f"\n--- Data Generation Round {round_num} ---")
        for device in devices:
            msg = device.generate_data()
            ingestion_service.ingest(msg)
        # Process all messages currently in the queue.
        processing_engine.process_messages()

    # Query and print the stored data.
    stored_data = storage_service.query_data()
    print("\nFinal stored data:")
    for data in stored_data:
        print(data)
