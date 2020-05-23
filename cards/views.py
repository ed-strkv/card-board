from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Tag, Card, Task
from .forms import ModelTagForm, ModelCardAddForm, ModelCardEditForm, ModelTaskForm, CreateUserForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group

@unauthenticated_user
def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='users')
            user.groups.add(group)
            messages.success(request, 'Account was created for ' + username)
            return redirect('login_page')
    context = {'form': form}
    return render(request, "cards/register.html", context)

@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password is incorrect')         
    return render(request, 'cards/login.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('login_page')

@login_required(login_url='login_page')
def home(request):
    tags = Tag.objects.all().filter(user=request.user)
    if request.method == "POST":
        form = ModelTagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            print(tag.title)
            tag.save()
            messages.success(request, "tag '%s' has been added" %tag.title)
            return redirect('home')
    else:
        form = ModelTagForm()
    context = {"tags": tags}
    return render(request, "cards/home.html", context)

@login_required
def tag_edit(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    cards = Card.objects.filter(tag__id=pk)
    if request.method == "POST":
        form = ModelTagForm(request.POST, instance=tag)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            messages.success(request, "tag '%s' has been changed" %tag.title)
            return redirect('home')
    else:
        form = ModelTagForm(instance=tag)
    return render(request, 'cards/tag_edit.html', {'form': form, 'tag': tag})

@login_required
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    cards = Card.objects.filter(tag__id=pk)
    if request.method == "POST":
        for card in cards:
            card.card_image.delete()
        tag.delete()
        messages.success(request, "tag '%s' has been deleted" %tag.title)
        return redirect('home')
    return render(request, 'cards/tag_delete.html', {'tag': tag})

@login_required
def add_card(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        form = ModelCardAddForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.tag = tag
            form.save()
            messages.success(request, "card '%s' has been added" %card.title)
            return redirect('home')
    else:
        form = ModelCardAddForm(initial={"tag": tag})
    return render(request, 'cards/add_card.html', {'form': form})



@login_required
def card_edit(request, pk):
    card = get_object_or_404(Card, pk=pk)
    card_tag = card.tag
    all_tags = Tag.objects.all()
    if request.method == "POST":
        form = ModelCardEditForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            card = form.save(commit=False)
            card.save()
            messages.success(request, "card '%s' has been changed" %card.title)
            return redirect('card_detail', card.id)
    else:
        form = ModelCardEditForm(instance=card)
    return render(request, 'cards/card_edit.html', {'form': form, 'card': card, 'card_tag': card_tag, 'all_tags': all_tags})



@login_required
def card_delete(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if request.method == "POST":
        card.delete()
        messages.success(request, "card '%s' has been deleted" %card.title)
        return redirect('home')
    return render(request, 'cards/card_delete.html', {'card': card})

@login_required
def card_detail(request, pk):
    card = get_object_or_404(Card, pk=pk)
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
               'all_tasks': all_tasks,
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
            messages.success(request, "task '%s' has been added" %task.title)
            return redirect('card_detail', card.id)
    return render(request, 'cards/card_detail.html', context)

@login_required
def task_doing(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = "doing"
    task.save()
    messages.success(request, "task '%s' is in progress" %task.title)
    return redirect('card_detail', task.card_id)

@login_required
def task_done(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = "done"
    task.save()
    messages.success(request, "task '%s' has been done" %task.title)
    return redirect('card_detail', task.card_id)

@login_required
def task_delete(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    messages.success(request, "task '%s' has been deleted" %task.title)
    return redirect('card_detail', task.card_id)

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = ModelTaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            messages.success(request, "task '%s' has been changed" %task.title)
            return redirect('card_detail', task.card.id)
    else:
        form = ModelTaskForm(instance=task)
    return render(request, 'cards/task_edit.html', {'form': form, 'task': task})