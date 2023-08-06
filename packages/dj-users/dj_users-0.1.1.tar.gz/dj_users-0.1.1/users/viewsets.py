""" ViewSets """


from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsOwner
from users.serializers import UserSerializer, UserCreationSerializer, UserUpdateSerializer


# Create your viewsets here.
User = get_user_model()


class UserViewSet(ModelViewSet):
    """ User ViewSet """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_permissions(self):
        """ Return permissions """

        if self.action == 'create':
            self.permission_classes = []

        return super().get_permissions()

    def get_serializer_class(self):
        """ Return serializer  """

        if self.action == 'create':
            self.serializer_class = UserCreationSerializer

        if self.action in ('update', 'partial_update'):
            self.serializer_class = UserUpdateSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        """ Encrypt the password """

        serializer.save(
            password=make_password(
                serializer.validated_data['password']
            )
        )
