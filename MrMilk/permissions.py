""" The rest framework provides us with a base class that we use to
make custom permissions classes"""

from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """allow users to edit their own profile"""

    # we add has_object_permissions function , it gets called every time a request is made to our
    # API that we assign our permissions
    def has_object_permission(self, request, view, obj):
        """check user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id
