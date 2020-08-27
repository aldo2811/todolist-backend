from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Todolist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="todolist")

    def __str__(self):
        return self.user.username + "'s Todolist"


class Category(models.Model):
    todolist = models.ForeignKey(
        Todolist, on_delete=models.CASCADE, related_name="category"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Task(models.Model):
    STATUS = (
        (1, _('High')),
        (2, _('Normal')),
        (3, _('Low'))
    )

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="task"
    )
    todolist = models.ForeignKey(
        Todolist, on_delete=models.CASCADE, related_name="task"
    )
    priority = models.PositiveSmallIntegerField(choices=STATUS, default=2)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    datetime_created = models.DateTimeField()
    date_due = models.DateField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.datetime_created = timezone.now()
        return super(Task, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_todolist(sender, instance, created, **kwargs):
    if created:
        Todolist.objects.create(user=instance)
