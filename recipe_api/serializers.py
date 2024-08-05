from rest_framework import serializers
from .models import Recipe
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['recipe_id', 'name', 'description', 'ingredients', 'steps', 'image_url', 'timestamp', 'updated', 'user_id']

