from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Todolist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="todolist")

    def __str__(self):
        return self.user.username + "'s Todolist"


class Task(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="task"
    )
    todolist = models.ForeignKey(
        Todolist, on_delete=models.CASCADE, related_name="task"
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_due = models.DateTimeField()

    def __str__(self):
        return self.title


@receiver(post_save, sender=User)
def create_todolist(sender, instance, created, **kwargs):
    if created:
        Todolist.objects.create(user=instance)
