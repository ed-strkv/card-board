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
    tags = Tag.objects.all().filter(user=request.user)
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

def add_card(request, pk):
    tag = Tag.objects.get(id=pk)

    if request.method == "POST":
        form = ModelCardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.tag = tag
            form.save()
            return redirect('home')
    else:
        form = ModelCardForm(initial={"tag": tag})
    return render(request, 'cards/add_card.html', {'form': form})

def edit_card(request, pk):
    card = Card.objects.get(id=pk)
    if request.method == "POST":
        form = ModelCardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            card = form.save(commit=False)
            card.save()
            return redirect('home')
    else:
        form = ModelCardForm(instance=card)
    return render(request, 'cards/edit_card.html', {'form': form, 'card': card})


def add_task(request, pk):
    author = request.user
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        form = ModelTaskForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            task = Task()
            task.name = data["name"]
            task.description = data["description"]
            task.created_date = timezone.now()
            task.status = data["status"]
            task.priority = data["priority"]
            task.user_name = request.user
            project = Project()
            task.project = Project.objects.get(id=pk)
            task.save()
            messages.success(request, "Добавлена задача '%s'" %task.name)
            return redirect("/project/%d/task_list/" %task.project.id)
    else:
        form = ModelTaskForm(initial={"user_name": author, "priority": "5"})
    return render(request, "projects/add_task.html", {"form": form, "project": project})


edit_card


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