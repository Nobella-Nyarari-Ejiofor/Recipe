"""
Views for the recipe api's
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet):
    """
    View for manage recipe API's
    """
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        """
        REtrieve recipe for authenticated user
        """
        return self.queryset.filter(user=self.request.user).order_by('-id')