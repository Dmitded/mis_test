from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == 'admin'


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == 'doctor'


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == 'patient'
