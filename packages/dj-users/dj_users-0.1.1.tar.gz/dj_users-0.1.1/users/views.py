""" Views """


from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from users.forms import UserForm
from users.mixins import OwnerMixin


# Create your views here.
User = get_user_model()


class UserCreateView(CreateView):
    """ User Create View """

    model = User
    form_class = UserCreationForm

    def get_success_url(self):
        """ Return the URL to redirect to after processing a valid form. """

        instance = self.object

        return reverse_lazy('users:update', args=[instance.id])


class UserListView(LoginRequiredMixin, ListView):
    """ User List View """

    model = User
    paginate_by = 100


class UserDetailView(LoginRequiredMixin, OwnerMixin, DetailView):
    """ User Detail View """

    model = User
    pk_url_kwarg = 'id'


class UserUpdateView(LoginRequiredMixin, OwnerMixin, UpdateView):
    """ User Update View """

    model = User
    pk_url_kwarg = 'id'
    form_class = UserForm


class UserDeleteView(LoginRequiredMixin, OwnerMixin, DeleteView):
    """ User Delete View """

    model = User
    pk_url_kwarg = 'id'
