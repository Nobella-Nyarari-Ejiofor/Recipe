# flake8: noqa
"""
Views for the recipe api's
"""
from rest_framework import (
    viewsets,
    mixins ,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe , Tag , Ingredient
from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet):
    """
    View for manage recipe API's
    """
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        """
        REtrieve recipe for authenticated user
        """
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """
        Return teh serializer class for request
        """
        if self.action =='list':
            return serializers.RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """
        create a new recipe
        """
        serializer.save(user = self.request.user)

#by using mixin.UpdateModelMixin we do not need to create code for updating the tags list
class TagViewSet(mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin , 
                 viewsets.GenericViewSet):
    """
    Manage tags in the database
    """
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter queryset to authenticated user .
        """
        return self.queryset.filter(user = self.request.user).order_by('-name')

class IngredientViewSet(mixins.ListModelMixin ,
                        viewsets.GenericViewSet,
                        mixins.UpdateModelMixin):
     """
     Manage ingredients in the database
     """
     serializer_class = serializers.IngredientSerializer
     queryset = Ingredient.objects.all()
     authentication_classes = [TokenAuthentication]
     permission_classes = [IsAuthenticated]

     def get_queryset(self):
        """
        Filter queryset to authenticated user 
        """
        return Ingredient.objects.filter(user = self.request.user).order_by('-name')

                                               

