from rest_framework.permissions import BasePermission, SAFE_METHODS 
class IsOwnerOrReadOnly(BasePermission): 
    """Allow owners to edit/delete; others read-only. Applied to Patient resources.""" 
    def has_object_permission(self, request, view, obj): 
        if request.method in SAFE_METHODS: 
            return True 
        return getattr(obj, "created_by_id", None) == getattr(request.user, "id", None)