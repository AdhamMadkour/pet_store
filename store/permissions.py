from rest_framework import permissions
from .models import Pet


class OwnerOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        Pet_id = view.kwargs.get("pk")
        pet = Pet.objects.select_related("owner").get(id=Pet_id)
        return pet.owner == request.user


class IsOwnerOfThePet(permissions.BasePermission):
    def has_permission(self, request, view):
        pet = Pet.objects.get(id=view.kwargs.get("pet_pk"))
        return pet.owner == request.user
