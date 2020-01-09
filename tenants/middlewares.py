from tenants.utils import set_tenant_schema_for_request
from django.http import HttpResponse


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        schema_is_connected = set_tenant_schema_for_request(request)
        if schema_is_connected:
            response = self.get_response(request)
            return response
        else:
            return HttpResponse('Schema not found', status=404)
