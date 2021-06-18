from rest_framework import permissions


class CreatorOrAdminPermission(permissions.BasePermission):
    message = 'Это могут делать только создатель и администратор'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator or request.user.is_staff


class OrderCreatePermission(permissions.BasePermission):
    message = 'Нельзя указывать статус заказа при создании'

    def has_permission(self, request, view):
        return not request.data.get('status', False)


class OrderUpdatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        elif request.data.get('status', False):
            self.message = 'Менять статус заказа может только администратор'
            return False
        else:
            self.message = 'Клиент может изменят и удалать только новые заказы'
            return obj.status == "NEW"
