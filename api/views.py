from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TodoSerializer
from .db import todos_collection
from bson import ObjectId
from datetime import datetime

class TodoListCreate(APIView):
    def get(self, request):
        todos = []
        for doc in todos_collection.find():
            doc['id'] = str(doc['_id'])
            todos.append(doc)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            todo_data = serializer.validated_data
            todo_data['created_at'] = datetime.now()
            result = todos_collection.insert_one(todo_data)
            
            todo_data['id'] = str(result.inserted_id)
            return Response(TodoSerializer(todo_data).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoRetrieveUpdateDestroy(APIView):
    def get_object(self, pk):
        try:
            return todos_collection.find_one({'_id': ObjectId(pk)})
        except:
            return None

    def get(self, request, pk):
        doc = self.get_object(pk)
        if not doc:
            return Response(status=status.HTTP_404_NOT_FOUND)
        doc['id'] = str(doc['_id'])
        return Response(TodoSerializer(doc).data)

    def patch(self, request, pk):
        doc = self.get_object(pk)
        if not doc:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = TodoSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            update_data = serializer.validated_data
            todos_collection.update_one(
                {'_id': ObjectId(pk)},
                {'$set': update_data}
            )
            # Fetch updated doc
            updated_doc = todos_collection.find_one({'_id': ObjectId(pk)})
            updated_doc['id'] = str(updated_doc['_id'])
            return Response(TodoSerializer(updated_doc).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        result = todos_collection.delete_one({'_id': ObjectId(pk)})
        if result.deleted_count == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
