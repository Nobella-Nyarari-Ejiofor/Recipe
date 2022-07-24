# flake8: noqa
"""
Seriallizers for the API View . NOte serializers convert python objects to json or vice versa
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from rest_framework import serializers
from django.utils.translation import gettext as _


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


    def update(self,instance , validated_data):
        """
        Update and return user 
        """
        password = validated_data.pop('password', None)
        #we leverage existing logic from modelserializer to update the instance 
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user



class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for the auth token
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': ' password'},
        trim_whitespace = False
    )

    def validate(self,attrs):
        #getting attributes from the api end point 
        email = attrs.get('email')
        password = attrs.get('password')
        #built in method thatv authenticates a user if credentials are valid if not returns an empty object
        user = authenticate(
            #for formality
            request= self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code ='authorization')

        attrs['user'] = user

        return attrs


