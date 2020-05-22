from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.user)


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

    def delete(self, *args, **kwargs):
        self.card_image.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = Card.objects.get(id=self.id)
            if this.card_image != self.card_image:
                this.card_image.delete(save=False)
        except: 
            pass # when new photo then we do nothing, normal case          
        super(Card, self).save(*args, **kwargs)

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