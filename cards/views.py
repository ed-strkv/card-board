from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Tag, Card, Task

def home(request):
	tags = Tag.objects.filter(user=request.user)
	context = {'tags': tags}
	cards = Card.objects.filter()
	tasks = Task.objects.filter()
	return render(request, 'cards/home.html', context)

def card_detail(request, pk):
	card = Card.objects.get(id=pk)
	
	tasks_todo = Task.objects.filter(card_id=pk, status="todo")
	tasks_doing = Task.objects.filter(card_id=pk, status="doing")
	tasks_done = Task.objects.filter(card_id=pk, status="done")
	
	context = {'card': card,
			   'tasks_todo': tasks_todo,
			   'tasks_doing': tasks_doing,
			   'tasks_done': tasks_done
			  }
	return render(request, 'cards/card_detail.html', context)

def task_detail(request, pk):
	task = Task.objects.get(id=pk)
	context = {'task': task}
	return render(request, 'cards/task_detail.html', context)