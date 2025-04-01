from django.urls import path
from .views import chat_room,front_page,register
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [

    path("chat/<str:room_name>/", chat_room, name="chat_room"),
    path('',front_page,name='front_page'),
    path('register/', register, name='register'),
      path('login/', auth_views.LoginView.as_view(), name='login'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
