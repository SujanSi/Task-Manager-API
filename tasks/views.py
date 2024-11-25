from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Task
from .serializers import TaskSerializer

# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])

def signup_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.create_user(username=username, password=password)
    user.save()

    token = Token.objects.create(user=user)  # Create a token for the new user

    return Response({'message': 'User created successfully.', 'token': token.key}, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([AllowAny])

def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username= username, password=password)
    if user is None:
        return Response({'error':'Invalid creditial'}, status=status.HTTP_401_UNAUTHORIZED)
    
    token,created = Token.objects.get_or_create(user = user)
    return Response({'message': 'Login successful.', 'token': token.key}, status=status.HTTP_200_OK)

@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def task_list(request):
    if request.method == "GET":
        tasks = Task.objects.filter(user = request.user)
        serializer = TaskSerializer(tasks, many = True)
        return Response(serializer.data)
    
    if request.method == "POST":
        serializer = TaskSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data , status= status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)  # Ensure the task belongs to the logged-in user
    except Task.DoesNotExist:
        return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TaskSerializer(task, data=request.data, partial=True)  # Allow partial updates
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)  # Ensure the task belongs to the logged-in user
    except Task.DoesNotExist:
        return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)

    task.delete()
    return Response({'message': 'Task deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    