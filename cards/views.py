from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Tag, Card, Task
from .forms import ModelTagForm, ModelCardForm, ModelTaskForm
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
    if request.method == "POST":
        form = ModelTagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect('home')
    else:
        form = ModelTagForm()
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

def card_delete(request, pk):
    card = Card.objects.get(id=pk)
    
    if request.method == "POST":
        card.delete()
        messages.success(request, "Deleted")
        return redirect('home')

    return render(request, 'cards/card_delete.html', {'card': card})


def card_detail(request, pk):
    card = Card.objects.get(id=pk)
    context = {}

    tasks_todo = Task.objects.filter(card_id=pk, status="todo")
    tasks_doing = Task.objects.filter(card_id=pk, status="doing")
    tasks_done = Task.objects.filter(card_id=pk, status="done")

    all_tasks = Task.objects.filter(card_id=pk)

    counter_all_tasks = int(all_tasks.count())
    
    context = {'card': card,
               'tasks_todo': tasks_todo,
               'tasks_doing': tasks_doing,
               'tasks_done': tasks_done,
              }

    if counter_all_tasks >= 1:
        counter_doing = round(int(tasks_doing.count()*100)/counter_all_tasks)
        counter_done = round(int(tasks_done.count()*100)/counter_all_tasks)
        counter_todo = 100 - counter_doing - counter_done
        context['counter_doing'] = counter_doing
        context['counter_done'] = counter_done
        context['counter_todo'] = counter_todo


    if request.method == "POST":
        form = ModelTaskForm(request.POST, initial={"status": "todo", "card": card})
        if form.is_valid():
            task = form.save(commit=False)
            task.card = card
            form.save()
            context['form'] = form
            return redirect('card_detail', card.id)
    
    return render(request, 'cards/card_detail.html', context)



def task_doing(request, pk):
    task = Task.objects.get(id=pk)
    task.status = "doing"
    task.save()
    return redirect('card_detail', task.card_id)

def task_done(request, pk):
    task = Task.objects.get(id=pk)
    task.status = "done"
    task.save()
    return redirect('card_detail', task.card_id)


def task_delete(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()

    return redirect('card_detail', task.card_id)

def task_detail(request, pk):
    task = Task.objects.get(id=pk)
    context = {'task': task}
    return render(request, 'cards/task_detail.html', context)

"""
def task_add(request, pk):
    card = Card.objects.get(id=pk)

    if request.method == "POST":
        form = ModelTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.card = card
            form.save()
            return redirect('card_detail', card.id)
    else:
        form = ModelTaskForm(initial={"status": "todo", "card": card})
    return render(request, 'cards/add_task.html', {'form': form})
"""