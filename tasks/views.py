from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task
import json

# Create your views here.

@csrf_exempt
def task_list(request):
    if request.method == 'GET':
        tasks_qs = Task.objects.all.values('id', 'title', 'completed', 'created_at')
        #converting querylist to list
        tasks_list = list(tasks_qs)
        return JsonResponse (tasks_list, safe=False)


    if request.method == 'POST':
        #get data from request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error' : 'Invalid JSON'}, status =400)
        
        #extract the fields
        title = data.get('title')
        completed = data.get('completed', False)  #we put false so when we create a new task it takes false in the beginning as default

        #validate that title exists
        if not title:
            return JsonResponse ({'error': 'Title is required'}, status = 400)
        
        #create task in db
        task = Task.objects.create(title = title , completed = completed)

        #Return Sucess Message
        return JsonResponse({
            'message' : 'Task created successfully',
            'task' :{
                'id' : task.id,
                'title' : task.title,
                'completed': task.completed,
                'created_at': task.created_at.isoformat()
            }
        } , status = 201)
    return JsonResponse ({'error' : 'Method not allowed'}, status = 405)