from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Card(models.Model):
    tag = models.ForeignKey(Tag, null=True, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    card_image = models.ImageField(null=True, blank=True) #default="image.png"
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    card = models.ForeignKey(Card, null=True, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200, null=True)
    #deadline = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=8, choices=(('todo', 'todo'),
                                        ('doing', 'doing'),
                                        ('done', 'done')), default="todo")
    def __str__(self):
        return self.title

class Tutorial(models.Model):
    title = models.CharField(max_length=200, null=True)
    card_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title