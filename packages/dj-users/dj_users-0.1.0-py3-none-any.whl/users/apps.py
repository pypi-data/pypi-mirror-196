""" AppConf """


from django.apps import AppConfig


class UsersConfig(AppConfig):
    """ App Configuration for users app """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
