import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, ChannelNameRouter
from device_manager.consumers import BroadcastConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "channel": ChannelNameRouter({
        "udp-listener": BroadcastConsumer.as_asgi(),
    }),
})
