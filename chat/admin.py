from django.contrib import admin
from .models import ChatRoom, Message  # Import your models

admin.site.register(ChatRoom)
admin.site.register(Message)

