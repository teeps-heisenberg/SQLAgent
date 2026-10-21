"""
Example usage of SQLDBAgent demonstrating practical use cases.

Make sure to set your GEMINI_API_KEY environment variable or pass it directly.
"""

import utils.session
import os
from sqldb_agent import SQLDBAgent


def main():
    """Demonstrate SQLDBAgent capabilities."""

    # Initialize the agent
    # Option 1: Use environment variable GEMINI_API_KEY
    # Option 2: Pass API key directly: SQLDBAgent(api_key="your-api-key")
    try:
        agent = SQLDBAgent()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease set your GEMINI_API_KEY environment variable:")
        print("  export GEMINI_API_KEY='your-api-key-here'")
        return

    print("=" * 60)
    print("SQLDBAgent - Practical Demonstration")
    print("=" * 60)

    # Example 1: Generate SQL from natural language
    print("\n[1] Generating SQL from Natural Language")
    print("-" * 60)
    schema_info = """
    Tables:
    - users (id, name, email, created_at)
    - orders (id, user_id, amount, order_date)
    """
    result = agent.generate_sql(
        "Get all users who have placed orders with total amount greater than 1000",
        schema_info=schema_info
    )
    print(f"Request: {result['original_request']}")
    print(f"Generated SQL:\n{result['query']}")

    # Example 2: Explain a SQL query
    print("\n[2] Explaining SQL Query")
    print("-" * 60)
    sql_query = """
    SELECT u.name, SUM(o.amount) as total_spent
    FROM users u
    JOIN orders o ON u.id = o.user_id
    WHERE o.order_date >= '2024-01-01'
    GROUP BY u.id, u.name
    HAVING SUM(o.amount) > 1000
    ORDER BY total_spent DESC;
    """
    result = agent.explain_sql(sql_query)
    print(f"Query:\n{sql_query}")
    print(f"\nExplanation:\n{result['explanation']}")

    # Example 3: Optimize a SQL query
    print("\n[3] Optimizing SQL Query")
    print("-" * 60)
    slow_query = """
    SELECT * FROM users WHERE email LIKE '%@gmail.com';
    """
    result = agent.optimize_sql(slow_query)
    print(f"Original Query:\n{slow_query}")
    print(f"\nOptimized Query:\n{result['optimized_query']}")
    print(f"\nOptimization Notes:\n{result['optimization_notes']}")

    # Example 4: Validate SQL syntax
    print("\n[4] Validating SQL Query")
    print("-" * 60)
    test_query = """
    SELECT name, email FROM users WHERE id = 1;
    """
    result = agent.validate_sql(test_query)
    print(f"Query:\n{test_query}")
    print(f"Valid: {result['is_valid']}")
    print(f"Validation Notes:\n{result['validation_notes']}")

    print("\n" + "=" * 60)
    print("Demonstration Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

