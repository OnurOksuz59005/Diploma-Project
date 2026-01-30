from django.middleware.csrf import CsrfViewMiddleware
from django.utils.deprecation import MiddlewareMixin

class CustomCsrfMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            token = request.META.get('HTTP_X_CSRFTOKEN')
            if token:
                request.META['CSRF_COOKIE'] = token
        return None
