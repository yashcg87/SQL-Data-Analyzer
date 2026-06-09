def query_analyzer_prompt(table_names: list):
    # Convert list of tables into a readable string for the LLM
    available_tables = ", ".join([f'"{t}"' for t in table_names])
    
    QUERY_ANALYZER_PROMPT = f"""
    You are a query classifier and routing assistant.

    Your task is to analyze the user query and identify the routing path along with the target database table.

    Classification Options for "next_node":
    - "schema_retriever": if the query requires fetching data, metrics, attributes, or calculations from a database table.
    - "general_query": if the query is conversational, greetings, general knowledge, or completely unrelated to the database.

    Available Database Tables for "table_name":
    [{available_tables}]

    Rules:
    1. If "next_node" is "schema_retriever", match the intent of the query to the most logical table from the available tables list above.
    2. If "next_node" is "general_query", set the value of "table_name" to null.
    3. Do NOT include any markdown formatting, backticks (e.g., ```json), explanations, or whitespace outside the raw JSON object string.

    Output Format (STRICT JSON):
    {{"next_node": "schema_retriever" or "general_query", "table_name": "exact_table_name_from_list" or null}}
    """
    return QUERY_ANALYZER_PROMPT



def sql_generator(query: str, table_data: dict, feedback: str = "") -> str:
    """
    Generates a dynamic PostgreSQL prompt injecting current table data context 
    and validator feedback for self-correction loops.
    
    Args:
        query (str): The natural language question.
        table_data (Document): LangChain Document containing table schema metadata.
        feedback (str): Validation feedback explaining why the previous query failed (if any).
    """
    table_name = table_data.page_content
    columns_list = table_data.metadata.get("column_names", [])
    
    formatted_columns = f"({', '.join(columns_list)})" if columns_list else "Not provided"

    feedback_section = ""
    if feedback and feedback.strip():
        feedback_section = f"""
    ⚠️ PREVIOUS ATTEMPT FAILED VALIDATION:
    Your previous SQL query was rejected by the validator for the following reason:
    "{feedback.strip()}"
    
    CRITICAL CRITERIA FOR THIS ATTEMPT:
    You MUST modify your query structure to fully resolve the feedback issue stated above while still answering the user's original question.
        """

    SQL_GENERATOR_PROMPT = f"""
    You are an expert PostgreSQL query generator.

    Your task:
    Generate an optimal and correct SQL query for the given question.
    {feedback_section}
    Question: 
    "{query}"

    Context:
    - Database: PostgreSQL
    - Schema: SQL_ANALYZER
    - Table: {table_name}
    - Columns: {formatted_columns}

    Rules:
    1. Generate ONLY the executable SQL query string.
    2. Do NOT explain your logic and do NOT wrap the output in markdown code blocks like ```sql or ```.
    3. Use correct PostgreSQL syntax (e.g., table must be referenced as "SQL_ANALYZER".{table_name}).
    4. Use efficient queries (avoid unnecessary subqueries).
    5. Use JOIN only if required (such as self-join for manager references).
    6. Always SELECT only the required columns to answer the question (avoid SELECT *).
    7. Handle NULL values carefully (e.g., manager_id properties).
    8. If aggregation is involved, use GROUP BY properties properly.

    Output format:
    Return ONLY the raw SQL query text.
    """
    return SQL_GENERATOR_PROMPT




GENERAL_QUERY = """
        You are a helpful assistant.

        Your task:
        Answer the user's question in ONE clear and concise sentence.

        Rules:
        1. Keep it short and direct (1 sentence only)
        2. No extra explanation
        3. No formatting

        Output:
        A single sentence answer
        """


def validator(query: str, sql_query: str) -> str:
    """
    Generates a strict validation prompt to analyze the safety and accuracy of the generated SQL.
    
    Args:
        query (str): The user's original question (e.g., "what is the highest salary...")
        sql_query (str): The executable SQL string produced by the generator node.
    """
    VALIDATOR_PROMPT = f"""
    You are a SQL validation expert.

    Your task:
    Analyze the generated SQL query against the user's original question to ensure it is valid, safe, and logically correct.

    Inputs to Validate:
    - User Question: "{query}"
    - Generated SQL Query: {sql_query}

    Rules:
    1. The query must be syntactically correct for PostgreSQL.
    2. The query must strictly be read-only. It must NOT modify data (Forbidden: INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE).
    3. The query must only target the allowed schema tables and columns required to answer the question.
    4. The query must not contain dangerous operations or infinite loops.
    5. The query must be logically aligned with the user question (e.g., if asking for "highest salary", it should use MAX() or ORDER BY with LIMIT).

    Output format (STRICT JSON):
    Return ONLY a raw JSON object string with the following keys. Do NOT include markdown code blocks, backticks (e.g., ```json), or any conversational text.

    {{
        "pass": "YES" or "NO",
        "feedback": "Detailed reason why the validation failed, pointing out syntax errors, forbidden keywords, or logical mismatches. MUST be an empty string if pass is YES."
    }}
    """
    return VALIDATOR_PROMPT




EXECUTOR = """
        You are a result validator.

        Your task:
        Check if the database result correctly answers the user's question.

        Rules:
        1. Verify if the result is relevant to the question
        2. Ensure the result is not empty when data is expected
        3. Ensure the result logically matches the query intent

        Output:
        - YES → if result is correct
        - NO → if incorrect or irrelevant
        Do NOT explain
        """



def explainer(query: str, query_results: list) -> str:
    """
    Generates a response formatting prompt to turn raw SQL database rows 
    into a human-readable summary.
    
    Args:
        query (str): The user's original question (e.g., "what is the highest salary...")
        query_results (list): List of dictionaries returned by the executor node.
                              Example: [{"max_salary": 150000}]
    """
    EXPLAINER_PROMPT = f"""
    You are a response formatter.

    Your task:
    Convert the raw database output into a friendly, clear, and user-facing response.

    Inputs to Summarize:
    - User Question: "{query}"
    - Raw Database Output: {query_results}

    Rules:
    1. Your answer must directly and accurately address the user's question.
    2. Use simple, plain, and natural language.
    3. Keep it highly concise (2–3 sentences maximum).
    4. Highlight key technical metrics or values clearly (such as names, salary figures, positions, or counts).
    5. If the raw database output is an empty list [] or contains an error, politely inform the user that no records were found matching their request.

    Output format:
    Return ONLY the clean, final answer text. Do NOT include markdown styling or background information.
    """
    return EXPLAINER_PROMPT

