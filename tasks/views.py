from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
# Create your views here.

@api_view(['GET', 'POST'])
def task_list(request):
    if request == 'GET':
        #Get all tasks from the database
        tasks = Task.objects.all()
        #convert to JSON
        serializer = TaskSerializer(tasks,many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        #Get data from request
        serializer = TaskSerializer(data=request.data)
        #check if data is valid
        if serializer.is_valid():
            #Save to database
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PATCH','DELETE'])
def task_detail(request,pk):
    try:
        #Find the task by its ID(pk = primary_key)
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response (status=status.HTTP_404_NOT_FOUND)
    
    
    if request.method == 'GET':
        #Return the single task
        serializer =TaskSerializer(task)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        #Update the task with new data
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Delete the task
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)