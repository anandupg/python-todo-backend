from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from .models import Todo
from .serializers import TodoSerializer

class TodoListCreate(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

def hello_world(request):
    return JsonResponse({'message': 'Hello from Django!'})
