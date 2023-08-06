""" Forms """


from django import forms
from django.contrib.auth import get_user_model


# Create your forms here.
User = get_user_model()


class UserForm(forms.ModelForm):
    """ User Model Form """

    class Meta:
        """ Meta data """

        model = User
        exclude = [
            'id', 'password', 'is_superuser', 'is_staff', 'is_active',
            'groups', 'user_permissions', 'date_joined', 'last_login'
        ]
