import os
from django.core.management.base import BaseCommand
from django.conf import settings
from administration.utils.sql_utils import execute_sql

class Command(BaseCommand):

    def handle(self,*args, **kwargs):
        sql_file_path = os.path.join(settings.BASE_DIR, 'administration', 'sql', 'drop_all_tables.sql')
        if os.path.exists(sql_file_path):
            try:
                self.stdout.write("Deleting tables for entire project")
                execute_sql(sql_file_path)
                self.stdout.write(self.style.SUCCESS('Tables deleted successfully'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error deleting tables: {str(e)}'))
        else:
            self.stdout.write(self.style.ERROR('No SQL file found')) 
