""" Permissions """


from rest_framework.permissions import BasePermission


# Create your permissions here.
class IsOwner(BasePermission):
    """ Check the owner of the object """

    def has_object_permission(self, request, view, obj):
        """ Object permissions """

        return request.user == obj
