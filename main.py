import network
import time
from umqtt.simple import MQTTClient
from picozero import pico_temp_sensor
from machine import Pin

#Setup LED
led = Pin('LED', Pin.OUT)


# WiFi name and password
wifi_ssid = "wifi_name"
wifi_password = "wifi_pass"


# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(5)
print("Connected to WiFi")


# Adafruit IO Details
mqtt_host = "io.adafruit.com"
mqtt_username = "username"  # Username
mqtt_password = "topic_key"  # Key
mqtt_publish_topic = "publish_topic"  # MQTT Publish Topic
mqtt_subscribe_topic = "subscribe_topic" # MQTT Subscribe Topic


# Unique ID 
mqtt_client_id = "TotallyUniqueIDforMyIoTProjectSummer23"


# Initialize and connect to the MQTT server
mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host,
        user=mqtt_username,
        password=mqtt_password)


#Callback Function
def mqtt_subscription_callback(topic, message):
    if message == b'on':
        print("LED ON")
        led.value(1)
    elif message == b'off':
        print("LED OFF")
        led.value(0)


# Tell client to use callback and connect
mqtt_client.set_callback(mqtt_subscription_callback)
mqtt_client.connect()


# Initial value for LED is off
led.value(0)
mqtt_client.publish(mqtt_subscribe_topic, 'off')


# When connected, subscribe to MQTT topic
mqtt_client.subscribe(mqtt_subscribe_topic)
print('Connected and Subscribed')


try:
    while True:
        # Gathers data from the temperature sensor
        temperature = pico_temp_sensor.temp
        
        # Publish the data to the topic
        print(f'Publish {temperature:.2f}')
        mqtt_client.publish(mqtt_publish_topic, str(temperature))
        
        # Delay
        time.sleep(30)
        
except Exception as e:
    print('Failed to publish message')
finally:
    mqtt_client.disconnect()
