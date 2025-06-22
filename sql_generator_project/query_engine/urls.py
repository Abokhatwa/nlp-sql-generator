from django.urls import path
from .views import (
    generate_and_execute_sql,
    get_database_schema,
    get_query_history,
    get_database_stats
)

urlpatterns = [
    path('execute/', generate_and_execute_sql, name='execute_sql'),
    path('schema/', get_database_schema, name='get_schema'),
    path('history/', get_query_history, name='query_history'),
    path('stats/', get_database_stats, name='database_stats'),
]