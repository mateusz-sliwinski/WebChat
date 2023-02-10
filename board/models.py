from django.db import models


# Create your models here.
class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    image = models.ImageField(blank=True, null=True)
    body = models.TextField(blank=True, default='')
    owner = models.ForeignKey('Users', related_name='posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']
