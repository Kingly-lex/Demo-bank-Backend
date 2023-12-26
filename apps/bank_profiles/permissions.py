from rest_framework.permissions import BasePermission, SAFE_METHODS


class OnlyOwnerCanViewProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            request.user == obj.profile.user
        return False
