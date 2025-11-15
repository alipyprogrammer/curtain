from rest_framework.permissions import BasePermission ,SAFE_METHODS
from .models import User
from django.core.cache import cache
from rest_framework.response import Response

# class IsManger(BasePermission):
#     def has_object_permission(self ,request, view):
#         return bool( 
#             request.method in SAFE_METHODS or
#             request.user and
#             request.user.Manager
#         )
def ip_lockdown(list_ip,time):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            dic_meta      = request.META
            list_dic_meta = list(dic_meta)
            if 'HTTP_X_FORWARDED_FOR' not in list_dic_meta:
                dic_meta['HTTP_X_FORWARDED_FOR'] = 'local'
            value = cache.get(f"ip-{dic_meta['HTTP_X_FORWARDED_FOR']}")

            if dic_meta['HTTP_X_FORWARDED_FOR'] in list_ip:
                return Response("ایپی شما مجاز نیست", status=429)

            if value:
                return Response("شما یه درخواست معتبر دارید", status=429 )
            else:
                cache.set(
                    f"ip-{dic_meta['HTTP_X_FORWARDED_FOR']}",
                    f"ip-{dic_meta['HTTP_X_FORWARDED_FOR']}",
                    timeout=time
                )
            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator



class IsManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.Manager)


class ISBlogManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.Manager or request.user.BlogManager )


class ISProductManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.Manager or request.user.ProductManager )

class ISOrderingManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.Manager or request.user.OrderingManager )

