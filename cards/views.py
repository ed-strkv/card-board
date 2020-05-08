from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Tag, Card, Task
from .forms import ModelTagForm, ModelCardForm
from django.contrib import messages

"""
def home(request):
    tags = Tag.objects.filter(user=request.user)
    context = {'tags': tags}
    cards = Card.objects.filter()
    tasks = Task.objects.filter()
    return render(request, 'cards/home.html', context)
"""
def home(request):
    tags = Tag.objects.all()
    context = {"tags": tags}
    return render(request, "cards/home.html", context)

def add_tag(request):
    if request.method == "POST":
        form = ModelTagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect('home')
    else:
        form = ModelTagForm()
    return render(request, 'cards/tag_add.html', {'form': form})

def tag_edit(request, pk):
    tag = Tag.objects.get(id=pk)
    
    if request.method == "POST":
        form = ModelTagForm(request.POST, instance=tag)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect('home')
    else:
        form = ModelTagForm(instance=tag)
    return render(request, 'cards/tag_edit.html', {'form': form, 'tag': tag})

def tag_delete(request, pk):
    tag = Tag.objects.get(id=pk)
    
    if request.method == "POST":
        tag.delete()
        messages.success(request, "Deleted")
        return redirect('home')

    return render(request, 'cards/tag_delete.html', {'tag': tag})


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

def add_card(request, pk):
    return render(request, 'cards/home.html')

