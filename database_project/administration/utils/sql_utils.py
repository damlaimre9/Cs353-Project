from django.db import connection

def execute_sql(file_path):
    with open(file_path, 'r') as file:
        sql_query = file.read()
    
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
