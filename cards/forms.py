from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tag, Card, Task

class ModelTagForm(forms.ModelForm):
	class Meta:
		model = Tag
		fields = ["title"]

class ModelCardAddForm(forms.ModelForm):
	class Meta:
		model = Card
		exclude = ['tag']

class ModelCardEditForm(forms.ModelForm):
	class Meta:
		model = Card
		fields = "__all__"

class ModelTaskForm(forms.ModelForm):
	class Meta:
		model = Task
		exclude = ["status", "card"]

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 
				  'email', 
				  'password1', 
				  'password2']