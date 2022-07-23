"""
Seriallizers for the API View . NOte serializers convert python objects to json or vice versa
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user oject
    """
    class Meta:
        model = get_user_model()
        fields = ['email','password','name']
        extra_kwargs = {'password':{'write_only' : True , 'min_length' : 5}}

    def create(self, validated_data):
        """
        create abd return a user with an encrypted password bby overriding the default get_user_model
        """
        return get_user_model().objects.create_user(**validated_data)

        