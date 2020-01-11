from django.core.management.commands.migrate import Command as MigrationCommand

from django.db import connection
from ...utils import get_tenants_map, get_public_schema_name, get_shared_apps


class Command(MigrationCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            print(options)
            options['public'] = False
            schemas = get_tenants_map().values()
            for schema in schemas:
                cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
                cursor.execute(f"SET search_path to {schema}")
                super(Command, self).handle(*args, **options)

            options['public'] = True
            public_schema = get_public_schema_name()
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {public_schema}")
            cursor.execute(f"SET search_path to {public_schema}")
            super(Command, self).handle(*args, **options)
