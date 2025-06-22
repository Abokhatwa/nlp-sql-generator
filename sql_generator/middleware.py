from django.utils.cache import add_never_cache_headers
from django.utils.deprecation import MiddlewareMixin

class NoCacheMiddleware(MiddlewareMixin):
    """Middleware to prevent caching of sensitive pages"""
    
    def process_response(self, request, response):
        # Add no-cache headers to dashboard and API endpoints
        if request.path.startswith('/dashboard') or request.path.startswith('/api'):
            add_never_cache_headers(response)
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response