from rest_framework.permissions import BasePermission

class isOwnerAndAdmin(BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the 'OWNER' role and 'is_admin set to true
        return request.user and request.user.role == 'OWNER' and request.user.is_admin
