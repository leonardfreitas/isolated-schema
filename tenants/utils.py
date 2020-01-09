from django.db import connection


def hostname_from_request(request):
    # split on `:` to remove port
    # agenda.com
    # levi.agenda.com:8000
    # levi.agenda.com
    return request.get_host().split(":")[0].lower()


def tenant_schema_from_request(request):
    # levi.agenda.com
    hostname = hostname_from_request(request)
    tenants_map = get_tenants_map()
    return tenants_map.get(hostname, False)


def set_tenant_schema_for_request(request):
    schema_founded = tenant_schema_from_request(request)
    if schema_founded:
        with connection.cursor() as cursor:
            cursor.execute(f"SET search_path to {schema_founded}")
        return True
    return False


def get_tenants_map():
    return {"thor.localhost": "thor", "potter.localhost": "potter"}
    # return {"thor.polls.local": "thor", "poter.polls.local": "potter"}
