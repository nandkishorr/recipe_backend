from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Recipe
from .serializers import RecipeSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class RecipeListApiView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]
    

    def get(self, request, *args, **kwargs):
     
        recipes = recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
       
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'ingredients': request.data.get('ingredients'),
            'steps': request.data.get('steps'),
            'image_url': request.data.get('image_url'),
            'user_id': request.data.get('user_id')
        }
        # print (request.data.get('user_id'))
        serializer = RecipeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RecipeDetailApiView(APIView):

    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]
    def get_object(self, recipe_id):
      
        try:
            return Recipe.objects.get(recipe_id=recipe_id)
        except Recipe.DoesNotExist:
            return None

    def get(self, request, recipe_id, *args, **kwargs):
      
        recipe_instance = self.get_object(recipe_id)
        if not recipe_instance:
            return Response(
                {"res": "Object with recipe id does not exist"},
                status=status.HTTP_404_NOT_FOUND  # Use 404 for not found
            )

        serializer = RecipeSerializer(recipe_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, recipe_id, *args, **kwargs):
       
        recipe_instance = self.get_object(recipe_id)
        if not recipe_instance:
            return Response(
                {"res": "Object with recipe id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'ingredients': request.data.get('ingredients'),
            'steps': request.data.get('steps'),
            'image_url': request.data.get('image_url'),
            # 'user_id': request.data.get('user_id')if request.user.is_authenticated else None
        }
       
        serializer = RecipeSerializer(instance=recipe_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id, *args, **kwargs):
        '''
        Deletes the Recipe item with the given recipe_id if it exists
        '''
        recipe_instance = self.get_object(recipe_id)
        if not recipe_instance:
            return Response(
                {"res": "Object with recipe id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        recipe_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    

class RecipeSearchView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]
    def get(self, request, *args, **kwargs):
        '''
        Searches for recipes by name and ingredients
        '''
        name = request.query_params.get('value', None)
        ingredients = request.query_params.get('value', None)

       
        if not name and not ingredients:
            return Response(
                {"res": "Please provide a name or ingredients to search"},
                status=status.HTTP_400_BAD_REQUEST
            )

        
        query = Recipe.objects.all()
        if name:
            query = query.filter(name__icontains=name)
        if ingredients:
            ingredients_list = ingredients.split(',')
            for ingredient in ingredients_list:
                query = query.filter(ingredients__icontains=ingredient.strip())

       
        serializer = RecipeSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MockRandomRecipesView(APIView):
    """
    Mock function to select 5 random recipes from the database.
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]
    def get(self, request, *args, **kwargs):
       
        random_recipes = Recipe.objects.order_by('?')[:5]

        if not random_recipes:
            return Response(
                {"res": "No recipes available"},
                status=status.HTTP_404_NOT_FOUND
            )
        
       
        serializer = RecipeSerializer(random_recipes, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)