from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class StaffOrServiceExemptThrottle(UserRateThrottle):
    scope = "user"

    def allow_request(self, request, view):
        if request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            return True


        if request.headers.get("X-INTERNAL-TOKEN") == "MY_SECRET_SERVICE_TOKEN":
            return True

        return super().allow_request(request, view)
