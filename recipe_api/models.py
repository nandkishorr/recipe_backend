from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    steps = models.TextField(blank=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
