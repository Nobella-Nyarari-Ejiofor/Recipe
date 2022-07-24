# flake8: noqa
# Create your views here.
from rest_framework import generics , authentication , permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer
)

class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system
    """
    serializer_class = UserSerializer

#ObtainAUthToken usualy provides a default view however uses username and password hence we customise it to use email and password
class CreateTokenView(ObtainAuthToken):
    """
    CReate a new auth token for user
    """
    serializer_class = AuthTokenSerializer
    #ENSURE USER INTERFACE IS ENABLED FOR THE VIEW ,,, DOESN'T ENABLE IT BY DEFAULT
    render_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Manage the authenticated user
    """
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAUthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieve and return the authenticated user
        """
        return self.request.user


