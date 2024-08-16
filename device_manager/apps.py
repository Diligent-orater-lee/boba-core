from django.apps import AppConfig
from django.conf import settings
import threading
import socket
import asyncio

class DeviceManagerConfig(AppConfig):
    name = 'device_manager'

    def ready(self):
        threading.Thread(target=self.start_udp_listener, daemon=True).start()

    def start_udp_listener(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('', settings.BROADCAST_PORT))
            sock.settimeout(1)
            print(f"Listening for broadcasts on port {settings.BROADCAST_PORT}")
        except socket.error as e:
            if e.errno != 98:
                print(e)

        while True:
            try:
                data, addr = sock.recvfrom(1024)
                print(f"Received data: {data}")
                if data.startswith(b"DISCOVER_ME:"):
                    slave_id = data.decode().split(":")[1]
                    print(f"Discovered slave {slave_id} at {addr[0]}")
                    self.respond_to_slave(addr[0], slave_id)
            except socket.timeout:
                pass
            except Exception as e:
                print(f"Error in broadcast listener: {e}")

    def respond_to_slave(self, slave_ip, slave_id):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = f"FOUND:{slave_id}"
        sock.sendto(message.encode(), (slave_ip, settings.BROADCAST_PORT))
        sock.close()
