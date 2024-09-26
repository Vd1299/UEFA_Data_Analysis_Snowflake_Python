# import snowflake.connector
# import json 

# def connect():
#     with open("creds.json") as f:
#         creds = json.load(f)

#     conn = snowflake.connector.connect(
#         user=creds['user'],
#         password=creds['password'],
#         account=creds['account'],
#     )
#     cur = conn.cursor()
#     try:
#         cur.execute("SELECT CURRENT_USER(), CURRENT_REGION();")
#         result = cur.fetchone()
#         print("Connected to Snowflake as:")
#         print(f"User: {result[0]}")
#         print(f"Region: {result[1]}")
        
#     except snowflake.connector.errors.Error as e:
#         print("Connection test failed:", e)
#     finally:
#         cur.close()
#     return conn

import snowflake.connector
import json 

def connect():
    with open("creds.json") as f:
        creds = json.load(f)

    conn = snowflake.connector.connect(
        user=creds['user'],
        password=creds['password'],
        account=creds['account'],
    )
    cur = conn.cursor()
    try:
        cur.execute("SELECT CURRENT_USER(), CURRENT_REGION();")
        result = cur.fetchone()
        print("Connected to Snowflake as:")
        print(f"User: {result[0]}")
        print(f"Region: {result[1]}")
        
    except snowflake.connector.errors.Error as e:
        print("Connection test failed:", e)
    finally:
        cur.close()  # Close cursor immediately after the connection test
    return conn
