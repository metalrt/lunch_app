from rest_framework import permissions


class EmployeePermission(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.user_type == 'employee' and request.method not in self.edit_methods:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        '''
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True
        '''

        if request.user.user_type == 'employee' and request.method not in self.edit_methods:
            return True

        return False


class RestaurantOwnerPermission(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.user_type == 'restaurant_owner' and request.method not in self.edit_methods:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        '''
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True
        '''

        if request.user.user_type == 'restaurant_owner' and request.method not in self.edit_methods:
            return True

        return False