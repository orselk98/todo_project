from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task
import json

# Create your views here.

@csrf_exempt
def task_list(request):

    if request.method == 'GET':
        #Check if user wants to filter by completed status
        completed = request.GET.get('completed')

        if completed is not None:
            completed_bool = completed.lower() == 'true'
            tasks_qs = Task.objects.filter(completed=completed_bool).values('id', 'title', 'completed', 'created_at', 'priority')
        else:
            tasks_qs = Task.objects.all().values('id', 'title', 'completed', 'created_at', 'priority')
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
        completed = data.get('completed', False) #we put false so when we create a new task it takes false in the beginning as default
        priority = data.get('priority', 'medium')

        #validate that title exists
        if not title:
            return JsonResponse ({'error': 'Title is required'}, status = 400)
        #Validate if title is not empty
        if title.strip() =='':
            return JsonResponse ({'error': 'Title cannot be empty'}, status = 400)
        #validate if length of title is not more than 200
        if len(title)>200:
            return JsonResponse ({'error': 'Title cannot be more than 200 chars'}, status =400)
        #Validate priority value
        if priority not in ['low', 'medium', 'high']:
            return JsonResponse({'error': 'Invalid priority value'}, status=400)
        
        #create task in db
        task = Task.objects.create(title = title , completed = completed, priority=priority)

        #Return Sucess Message
        return JsonResponse({
            'message' : 'Task created successfully',
            'task' :{
                'id' : task.id,
                'title' : task.title,
                'completed': task.completed,
                'priority': task.priority,
                'created_at': task.created_at.isoformat()
            }
        } , status = 201)
    return JsonResponse ({'error' : 'Method not allowed'}, status = 405)

#Get , Patch , Delete a single task

@csrf_exempt
def task_detail (request, pk):
    #First lets try to find the task
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return JsonResponse ({'error':'Task Not Found'}, status =404)
    
    if request.method =='GET':
        #Return the single task
        task_dict ={
            'id' : task.id,
            'title':task.title,
            'completed' : task.completed,
            'priority' : task.priority,
            'created_at' : task.created_at.isoformat()
        }
        return JsonResponse(task_dict, safe=False)
    

    if request.method == 'PATCH':
        #get data from request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse ({'error': 'Invalid JSON'},status=400)
        
        #extract the files
        title = data.get('title')
        completed =data.get('completed')
        priority = data.get('priority')


        #update the task fields
        if title:
            task.title = title
        if completed is not None: #check for none because false is avalid value
            task.completed= completed
        if priority:
            if priority not in ['low', 'medium', 'high']:
                return JsonResponse({'error': 'Invalid priority value'}, status=400)
            task.priority = priority

        #save to db
        task.save()

        #Return success message
        return JsonResponse ({
            'message' : 'Task updated sucessfully',
            'task' : {
                'id' : task.id,
                'title' : task.title,
                'completed' : task.completed,
                'priority' : task.priority,
                'created_at' : task.created_at.isoformat()
            }
        })
    if request.method == 'DELETE':
        #delete the task
        task.delete()
        return JsonResponse({'message' : 'Task deleted successfully'}, status =204)
    
    return JsonResponse({'error' : 'Method not allowed'}, status =405)
