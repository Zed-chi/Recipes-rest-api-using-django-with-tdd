from rest_framework import generics
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """ Create new user in system """
    serializer_class = UserSerializer
