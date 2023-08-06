""" URLConf """


from django.urls import path

from users.views import UserCreateView, UserDetailView, UserListView, UserUpdateView, UserDeleteView


# Create your patterns here.
app_name = 'users'


urlpatterns = [
    path(
        '',
        UserListView.as_view(),
        name='list'
    ),
    path(
        'register/',
        UserCreateView.as_view(),
        name='create'
    ),
    path(
        '<int:id>/',
        UserDetailView.as_view(),
        name='detail'
    ),
    path(
        '<int:id>/update/',
        UserUpdateView.as_view(),
        name='update'
    ),
    path(
        '<int:id>/delete/',
        UserDeleteView.as_view(),
        name='delete'
    ),
]
