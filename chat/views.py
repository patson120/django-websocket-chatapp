from django.shortcuts import render

# Create your views here.

def lobby(request, group):
    return render(request, 'chat/lobby.html')