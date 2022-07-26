# flake8: noqa
"""
Urls mapping for the recipe api app
"""

from django.urls import(
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]