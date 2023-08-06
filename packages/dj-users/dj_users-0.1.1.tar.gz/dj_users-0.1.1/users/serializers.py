""" Serializers """


from django.contrib.auth import get_user_model
from rest_framework import serializers


# Create your serializers here.
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """ User Serializer """

    class Meta:
        """ Meta data """

        model = User
        exclude = ['password', 'groups', 'user_permissions']


class UserCreationSerializer(UserSerializer):
    """ User Creation Serializer """

    class Meta(UserSerializer.Meta):
        """ Meta data """

        exclude = [
            'id', 'is_superuser', 'is_staff', 'is_active',
            'groups', 'user_permissions', 'date_joined', 'last_login'
        ]


class UserUpdateSerializer(UserSerializer):
    """ User Update Serializer """

    class Meta(UserSerializer.Meta):
        """ Meta data """

        exclude = [
            'id', 'password', 'is_superuser', 'is_staff', 'is_active',
            'groups', 'user_permissions', 'date_joined', 'last_login'
        ]
