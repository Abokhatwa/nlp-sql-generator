from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import pandas as pd
import sqlite3
import json
import os
from django.conf import settings
import time
from .sql_generator import SQLGenerator
from .database_schemas import DATABASES, get_schema_prompt
from authentication.models import QueryLog

# Database file mapping
DB_FILE_MAPPING = {
    "E-Commerce": "databases/ecommerce.db",
    "Hospital Management": "databases/hospital.db",
    "School Management": "databases/school.db"
}

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_and_execute_sql(request):
    try:
        natural_language_query = request.data.get('query')
        database_name = request.data.get('database')
        
        if not natural_language_query or not database_name:
            return Response({
                'success': False,
                'error': 'Query and database name are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user has access to the database
        if not request.user.can_access_database(database_name.lower().replace(' ', '_').replace('-', '')):
            return Response({
                'success': False,
                'error': 'You do not have access to this database'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Initialize SQL Generator
        sql_generator = SQLGenerator()
        
        # Get schema for selected database
        schema = get_schema_prompt(database_name)
        
        # Generate SQL
        result = sql_generator.generate_sql(
            natural_language_query=natural_language_query,
            schema=schema,
            database_name=database_name
        )
        
        if not result['success']:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Execute query
        start_time = time.time()
        df, error = execute_query(result['sql_query'], database_name)
        execution_time = time.time() - start_time
        
        # Log the query
        query_log = QueryLog.objects.create(
            user=request.user,
            natural_language_query=natural_language_query,
            generated_sql=result['sql_query'],
            database_name=database_name,
            execution_time=execution_time,
            row_count=len(df) if df is not None else 0,
            success=error is None,
            error_message=error
        )
        
        if error:
            return Response({
                'success': False,
                'error': error
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Convert DataFrame to JSON
        data = df.to_dict(orient='records')
        columns = list(df.columns)
        
        return Response({
            'success': True,
            'sql_query': result['sql_query'],
            'explanation': result['explanation'],
            'data': data,
            'columns': columns,
            'row_count': len(df),
            'execution_time': round(execution_time, 3)
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def execute_query(sql_query, database_name):
    """Execute SQL query and return results"""
    try:
        db_path = os.path.join(settings.BASE_DIR, DB_FILE_MAPPING.get(database_name))
        if not db_path or not os.path.exists(db_path):
            return None, f"Database file not found: {db_path}"
        
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        
        return df, None
    except Exception as e:
        return None, str(e)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_database_schema(request):
    database_name = request.GET.get('database')
    
    if not database_name:
        return Response({
            'success': False,
            'error': 'Database name is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user has access
    if not request.user.can_access_database(database_name.lower().replace(' ', '_').replace('-', '')):
        return Response({
            'success': False,
            'error': 'You do not have access to this database'
        }, status=status.HTTP_403_FORBIDDEN)
    
    if database_name not in DATABASES:
        return Response({
            'success': False,
            'error': 'Invalid database name'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'success': True,
        'schema': DATABASES[database_name]
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_query_history(request):
    limit = int(request.GET.get('limit', 10))
    database = request.GET.get('database')
    
    queries = QueryLog.objects.filter(user=request.user)
    
    if database:
        queries = queries.filter(database_name=database)
    
    queries = queries[:limit]
    
    history = []
    for query in queries:
        history.append({
            'id': query.id,
            'natural_language': query.natural_language_query,
            'sql': query.generated_sql,
            'database': query.database_name,
            'row_count': query.row_count,
            'execution_time': query.execution_time,
            'success': query.success,
            'created_at': query.created_at.isoformat()
        })
    
    return Response({
        'success': True,
        'history': history
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_database_stats(request):
    database_name = request.GET.get('database')
    
    if not database_name:
        return Response({
            'success': False,
            'error': 'Database name is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user has access
    if not request.user.can_access_database(database_name.lower().replace(' ', '_').replace('-', '')):
        return Response({
            'success': False,
            'error': 'You do not have access to this database'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        db_path = os.path.join(settings.BASE_DIR, DB_FILE_MAPPING.get(database_name))
        if not os.path.exists(db_path):
            return Response({
                'success': False,
                'error': 'Database file not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        stats = {}
        for table_name in DATABASES[database_name]['tables'].keys():
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            stats[table_name] = count
        
        conn.close()
        
        return Response({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)