from rest_framework.permissions import BasePermission, SAFE_METHODS 
 
class IsOwnerOrAdmin(BasePermission): 
    """ 
    Permite editar/eliminar una subasta solo si el usuario es el propietario 
    o es administrador. Cualquiera puede consultar (GET). 
    """ 
 
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS: 
            return True 
        user = request.user

        if user.is_staff:
            return True

        if hasattr(obj, 'reviewer'):
            return obj.reviewer == user

        if hasattr(obj, 'auctioneer'):
            return obj.auctioneer == user

        return False