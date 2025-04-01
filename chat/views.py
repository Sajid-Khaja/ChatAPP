from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import UserProfile, ChatRoom, Message

# Chat Room view
def chat_room(request, room_name):
    room, _ = ChatRoom.objects.get_or_create(name=room_name)  # Get or create the chat room
    messages = Message.objects.filter(room=room).order_by("timestamp")  # Get messages for the room
    return render(request, "chat/chat_room.html", {"room_name": room_name, "messages": messages})

# Front page view
def front_page(request):
    return render(request, 'chat/front.html')  # Render the front page

# Register view for handling user registration and profile creation
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)  # Handle file uploads (e.g., profile picture)
        
        if form.is_valid():
            user = form.save()  # Save the user (without creating profile yet)
            
            # Check if the user already has a profile
            if not hasattr(user, 'profile'):
                profile = UserProfile.objects.create(user=user)  # Create a UserProfile for the new user
            
            # If an image is provided in the form, save it to the profile
            if form.cleaned_data.get('image'):
                profile.image = form.cleaned_data['image']
                profile.save()

            # Provide a success message and redirect the user to the login page
            messages.success(request, f'Your account has been created! You can now log in.')
            return redirect('login')  # Adjust the 'login' URL name if needed
    else:
        form = UserRegistrationForm()  # Create a new empty form

    return render(request, 'chat/register.html', {'form': form})  # Render the registration page with the form
