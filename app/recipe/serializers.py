# flake8: noqa
"""
SErializers for recipe api's
"""
from rest_framework import serializers

from core.models import Recipe , Tag

class TagSerializer(serializers.ModelSerializer):
    """
    serializer for tags
    """
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """
    serializer for recipes
    """ 
    tags = TagSerializer(many = True ,required = False)
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes','price','link','tags']
        read_only_fields = ['id']


    def create(self ,validated_data):
        """
        CReate a recipe where we can change the readonly attribute of the nested tag serializer
        """
        #code below removes the tags in the validated data
        tags = validated_data.pop('tags',[])
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)
        return recipe

class RecipeDetailSerializer(RecipeSerializer):
    """
    SErializer for recipe detail view
    """

    class Meta(RecipeSerializer.Meta):
        fields= RecipeSerializer.Meta.fields + ['description']


