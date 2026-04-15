# /// script
# dependencies = [
#   "paho-mqtt",
#   "psycopg2-binary",
# ]
# ///

import paho.mqtt.client as mqtt
import psycopg2
from datetime import datetime
import time
import sys

# --- Configuration ---
DB_CONFIG = "dbname=postgres user=postgres password=password host=localhost"
MQTT_BROKER = "localhost"
MQTT_PORT = 1883

class MQTTBridge:
    def __init__(self):
        self.db_conn = None
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

    def connect_db(self):
        try:
            if self.db_conn is None or self.db_conn.closed:
                self.db_conn = psycopg2.connect(DB_CONFIG)
                print("Database connected.")
        except Exception as e:
            print(f"Database connection failed: {e}")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
            client.subscribe("#")
        else:
            print(f"MQTT Connection refused with code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            self.connect_db()
            with self.db_conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO mqtt_logs (timestamp, topic, message) VALUES (%s, %s, %s)",
                    (datetime.now(), msg.topic, msg.payload.decode('utf-8', 'ignore'))
                )
                self.db_conn.commit()
        except Exception as e:
            print(f"Error saving message: {e}")
            if self.db_conn:
                self.db_conn.rollback()

    def run(self):
        while True:
            try:
                print(f"Attempting to connect to MQTT at {MQTT_BROKER}...")
                self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
                self.mqtt_client.loop_forever()
            except Exception as e:
                print(f"MQTT loop error: {e}. Retrying in 60 seconds...")
                time.sleep(60)

if __name__ == "__main__":
    bridge = MQTTBridge()
    bridge.run()
