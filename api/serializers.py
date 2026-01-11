from rest_framework import serializers

class TodoSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=200)
    completed = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(read_only=True, required=False)
