"""
SQLDBAgent - A practical demonstration using Google Gemini for SQL operations.

This module provides functionality to:
- Generate SQL queries from natural language
- Explain SQL queries
- Optimize SQL queries
- Validate SQL syntax
"""

import os
from typing import Optional, Dict, Any
import google.generativeai as genai


class SQLDBAgent:
    """SQL Database Agent using Google Gemini API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the SQLDBAgent with Gemini API.

        Args:
            api_key: Google Gemini API key. If not provided, will look for
                    GEMINI_API_KEY environment variable.
        """
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "API key is required. Provide it as argument or set "
                "GEMINI_API_KEY environment variable."
            )
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self._system_prompt = (
            "You are an expert SQL database administrator and query optimizer. "
            "You help with SQL query generation, explanation, optimization, and validation."
        )

    def generate_sql(
        self,
        natural_language_query: str,
        schema_info: Optional[str] = None,
        database_type: str = "PostgreSQL"
    ) -> Dict[str, Any]:
        """
        Generate SQL query from natural language description.

        Args:
            natural_language_query: Description of what SQL query is needed
            schema_info: Optional schema information (table names, columns, etc.)
            database_type: Type of database (PostgreSQL, MySQL, SQLite, etc.)

        Returns:
            Dictionary with generated SQL and explanation
        """
        prompt = f"""
{self._system_prompt}

Task: Generate a SQL query for {database_type} database.

User Request: {natural_language_query}
"""
        if schema_info:
            prompt += f"\nSchema Information:\n{schema_info}\n"

        prompt += "\nProvide only the SQL query. Do not include explanations in the query."

        try:
            response = self.model.generate_content(prompt)
            sql_query = response.text.strip()
            
            # Clean up the SQL query (remove markdown formatting if present)
            if sql_query.startswith("```sql"):
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            elif sql_query.startswith("```"):
                sql_query = sql_query.replace("```", "").strip()

            return {
                "query": sql_query,
                "status": "success",
                "original_request": natural_language_query
            }
        except Exception as e:
            return {
                "query": None,
                "status": "error",
                "error": str(e),
                "original_request": natural_language_query
            }

    def explain_sql(self, sql_query: str) -> Dict[str, Any]:
        """
        Explain what a SQL query does in natural language.

        Args:
            sql_query: SQL query to explain

        Returns:
            Dictionary with explanation
        """
        prompt = f"""
{self._system_prompt}

Task: Explain the following SQL query in clear, natural language.

SQL Query:
{sql_query}

Provide a detailed explanation including:
1. What the query does
2. Which tables/columns are involved
3. Any joins, filters, or aggregations
4. The expected result structure
"""

        try:
            response = self.model.generate_content(prompt)
            explanation = response.text.strip()

            return {
                "query": sql_query,
                "explanation": explanation,
                "status": "success"
            }
        except Exception as e:
            return {
                "query": sql_query,
                "explanation": None,
                "status": "error",
                "error": str(e)
            }

    def optimize_sql(self, sql_query: str, performance_issues: Optional[str] = None) -> Dict[str, Any]:
        """
        Optimize a SQL query for better performance.

        Args:
            sql_query: SQL query to optimize
            performance_issues: Optional description of specific performance issues

        Returns:
            Dictionary with optimized query and optimization notes
        """
        prompt = f"""
{self._system_prompt}

Task: Optimize the following SQL query for better performance.

Original SQL Query:
{sql_query}
"""
        if performance_issues:
            prompt += f"\nKnown Performance Issues:\n{performance_issues}\n"

        prompt += """
Provide:
1. The optimized SQL query
2. A brief explanation of the optimizations made
3. Expected performance improvements
"""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()

            # Parse the response to extract query and explanation
            lines = result_text.split('\n')
            optimized_query = sql_query
            explanation = result_text

            # Try to extract SQL query if wrapped in code blocks
            if "```sql" in result_text:
                parts = result_text.split("```sql")
                if len(parts) > 1:
                    sql_part = parts[1].split("```")[0].strip()
                    optimized_query = sql_part
                    explanation = result_text.replace(f"```sql\n{sql_part}\n```", "").strip()

            return {
                "original_query": sql_query,
                "optimized_query": optimized_query,
                "optimization_notes": explanation,
                "status": "success"
            }
        except Exception as e:
            return {
                "original_query": sql_query,
                "optimized_query": None,
                "optimization_notes": None,
                "status": "error",
                "error": str(e)
            }

    def validate_sql(self, sql_query: str, database_type: str = "PostgreSQL") -> Dict[str, Any]:
        """
        Validate SQL query syntax and provide feedback.

        Args:
            sql_query: SQL query to validate
            database_type: Type of database (PostgreSQL, MySQL, SQLite, etc.)

        Returns:
            Dictionary with validation results
        """
        prompt = f"""
{self._system_prompt}

Task: Validate the following SQL query for {database_type} syntax and best practices.

SQL Query:
{sql_query}

Check for:
1. Syntax errors
2. Common mistakes
3. Best practices violations
4. Potential issues

Provide validation results.
"""

        try:
            response = self.model.generate_content(prompt)
            validation_result = response.text.strip()

            # Simple heuristic: if response mentions errors or issues, mark as warning
            is_valid = not any(
                keyword in validation_result.lower()
                for keyword in ["error", "invalid", "incorrect", "problem", "issue"]
            )

            return {
                "query": sql_query,
                "is_valid": is_valid,
                "validation_notes": validation_result,
                "status": "success"
            }
        except Exception as e:
            return {
                "query": sql_query,
                "is_valid": False,
                "validation_notes": None,
                "status": "error",
                "error": str(e)
            }

