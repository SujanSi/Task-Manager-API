from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_at', 'updated_at']  # Exclude 'user'
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']  # Prevent modification of these fields