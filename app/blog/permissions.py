from rest_framework import permissions


class IsOwnerOfObject(permissions.BasePermission):
    """The purpose of writing this class is to restrict
    admins from editing other admins' information"""

    def has_object_permission(self, request, view, obj):
        if request.method != 'GET':
            return obj.user == request.user
        return super(
            IsOwnerOfObject, self
        ).has_object_permission(request, view, obj)
