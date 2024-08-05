from django.urls import path
from .views import (
    RecipeListApiView,
    RecipeDetailApiView,
    RecipeSearchView,
    MockRandomRecipesView
)

urlpatterns = [
    path('', RecipeListApiView.as_view()),
    path('<int:recipe_id>/', RecipeDetailApiView.as_view()),
    path('search', RecipeSearchView.as_view(), name='recipe-search'),
    path('mock', MockRandomRecipesView.as_view())
]