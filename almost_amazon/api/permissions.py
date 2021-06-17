from rest_framework import permissions


class AuthorOrAdminPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author or request.user.is_staff


class ClientOrAdminPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.client or request.user.is_staff


class OrderCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.data.get('status', False)  # нельзя указывать статус заказа при создании


class OrderUpdatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        elif request.data.get('status', False):
            return False  # запрещены манипуляции со статусом всем кроме админов
        else:
            return obj.status == "NEW"  # клиент может изменят и удалать только новые заказы
