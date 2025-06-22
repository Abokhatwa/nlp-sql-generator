import openai
from typing import Optional
import os
from dotenv import load_dotenv
import re

load_dotenv()

class SQLGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def generate_sql(self, natural_language_query: str, schema: str, database_name: str) -> dict:
        """
        Generate SQL query from natural language using OpenAI API
        
        Args:
            natural_language_query: The user's natural language question
            schema: The database schema information
            database_name: Name of the selected database
            
        Returns:
            Dictionary with SQL query and explanation
        """
        
        system_prompt = f"""You are an expert SQL developer. Your task is to convert natural language queries into SQL queries.
        
You are working with a {database_name} database with the following schema:

{schema}

Rules:
1. Generate only valid SQL queries
2. Use proper SQL syntax
3. Include appropriate JOINs when needed
4. Use meaningful table aliases
5. Format the SQL query for readability
6. Provide a brief explanation of what the query does
7. If the query is ambiguous, make reasonable assumptions
8. Always return valid SQL that can be executed using Python's `sqlite3` module
9. If the user requests something that is not valid for the schema, return "saeed"

Return your response in the following format:
SQL_QUERY:
[Your SQL query here]

EXPLANATION:
[Brief explanation of what the query does]"""

        user_prompt = f"Convert this to SQL: {natural_language_query}"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            # Parse the response more robustly
            sql_query = ""
            explanation = ""
            
            # Split by SQL_QUERY and EXPLANATION markers
            if "SQL_QUERY:" in content:
                parts = content.split("SQL_QUERY:")
                if len(parts) > 1:
                    remaining = parts[1]
                    
                    if "EXPLANATION:" in remaining:
                        sql_parts = remaining.split("EXPLANATION:")
                        sql_query = sql_parts[0].strip()
                        if len(sql_parts) > 1:
                            explanation = sql_parts[1].strip()
                    else:
                        sql_query = remaining.strip()
            else:
                # If no markers, assume the entire response is SQL
                sql_query = content.strip()
            
            # Clean up SQL query - remove any markdown code blocks
            sql_query = re.sub(r'^```sql\s*', '', sql_query)
            sql_query = re.sub(r'^```\s*', '', sql_query)
            sql_query = re.sub(r'\s*```$', '', sql_query)
            sql_query = sql_query.strip()
            
            return {
                "success": True,
                "sql_query": sql_query,
                "explanation": explanation,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "sql_query": None,
                "explanation": None,
                "error": str(e)
            }
    
    def validate_api_key(self) -> bool:
        """Check if the OpenAI API key is valid"""
        try:
            self.client.models.list()
            return True
        except:
            return False