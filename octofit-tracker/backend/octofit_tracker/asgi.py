"""
ASGI config for octofit_tracker project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os


from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.generic.websocket import AsyncWebsocketConsumer
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')
django.setup()

# Simple echo consumer for /ws endpoint
class EchoConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		await self.accept()
		await self.send(text_data="WebSocket connection established.")

	async def disconnect(self, close_code):
		pass

	async def receive(self, text_data=None, bytes_data=None):
		await self.send(text_data=f"Echo: {text_data}")

application = ProtocolTypeRouter({
	"http": get_asgi_application(),
	"websocket": URLRouter([
		path("ws", EchoConsumer.as_asgi()),
		path("ws/", EchoConsumer.as_asgi()),
	]),
})
