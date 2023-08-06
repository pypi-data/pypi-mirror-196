""" Mixins """


from django.contrib.auth.mixins import UserPassesTestMixin


# Create your mixins here.
class OwnerMixin(UserPassesTestMixin):
    """ Check if the current logged in user is the owner of the object instance """

    def test_func(self):
        """ Test case """

        # Get the object
        instance = self.get_object()

        return self.request.user == instance
