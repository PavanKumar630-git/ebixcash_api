import pyodbc

insert_query_ebixcash = f"""
INSERT INTO ebixcashagentinfo (
    searchpincode,
    agency,
    agentname,
    contact,
    email,
    address,
    city,
    pincode
) VALUES (
    ?,?,?,?,
    ?,?,?,?
);
"""




def execute_insert_query(insert_query: str, params : any):
    """
    Executes a raw SQL INSERT query using the predefined connection string
    Handles errors and ensures proper connection cleanup

    Args:
        insert_query (str): Complete SQL INSERT statement to execute
    """
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=61.246.34.128,9042;"
        "DATABASE=PTS_B2B_TEST;"
        "UID=sa;"
        "PWD=Server$#@54321;"
        "TrustServerCertificate=yes;"
    )

    connection = None
    cursor = None

    print("QUERY:",insert_query)
    print("PARAMS:",params)

    try:
        # Validate the query
        if not insert_query.strip().upper().startswith("INSERT"):
            raise ValueError("Only INSERT queries are allowed")

        # Connect and execute
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()

        print(f"Executing: {insert_query[:100]}...")  # Log first 100 chars
        cursor.execute(insert_query,params)
        connection.commit()

        # Get results
        rowcount = cursor.rowcount
        print(f"**************************Query executed successfully. {rowcount} row(s) affected ***********************")

        return rowcount

    except pyodbc.Error as e:
        print(f"Database error: {str(e)}")
        if connection:
            connection.rollback()
        raise
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Connection closed")
