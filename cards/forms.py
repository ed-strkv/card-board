from django import forms
from .models import Tag, Card, Task

class ModelTagForm(forms.ModelForm):
	class Meta:
		model = Tag
		fields = ["title"]

class ModelCardForm(forms.ModelForm):
	class Meta:
		model = Card
		exclude = ["tag"]

class ModelTaskForm(forms.ModelForm):
	class Meta:
		model = Task
		exclude = ["status", "card"]