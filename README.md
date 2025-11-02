# SQLDBAgent - Gemini AI Demo

A practical demonstration of using Google Gemini for SQL database operations.

## Features

- **Generate SQL queries** from natural language descriptions
- **Explain SQL queries** in plain English
- **Optimize SQL queries** for better performance
- **Validate SQL syntax** and provide feedback

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Gemini API key:
```bash
export GEMINI_API_KEY='your-api-key-here'
```

Or create a `.env` file`:
```
GEMINI_API_KEY=your-api-key-here
```

## Usage

```python
from sqldb_agent import SQLDBAgent

# Initialize the agent
agent = SQLDBAgent()

# Generate SQL from natural language
result = agent.generate_sql(
    "Get all users who have placed orders",
    schema_info="users (id, name), orders (id, user_id, amount)"
)

# Explain a SQL query
result = agent.explain_sql("SELECT * FROM users WHERE id = 1")

# Optimize a SQL query
result = agent.optimize_sql("SELECT * FROM users WHERE email LIKE '%@gmail.com'")

# Validate SQL syntax
result = agent.validate_sql("SELECT name FROM users")
```

## Run Examples

```bash
python example_usage.py
```

## Requirements

- Python 3.7+
- Google Gemini API key

