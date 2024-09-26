

from Snowflake_connection import connect
import snowflake.connector

def load_data(cur):
    try:
        cur.execute("USE WAREHOUSE FOOTBALL_ANALYSIS;")
        cur.execute("USE DATABASE UEFA;")
        cur.execute("USE SCHEMA CHAMPIONS_LEAGUE;")

        csv_files = ['uefa_2020_converted.csv', 'uefa_2021_converted.csv', 'uefa_2022_converted.csv']
        for csv_file in csv_files:
            cur.execute(f"PUT file://{csv_file} @STAGING_AREA AUTO_COMPRESS=TRUE;")

        table_names = ['Data_2020', 'Data_2021', 'Data_2022']
        csv_file_names = ['uefa_2020_converted.csv', 'uefa_2021_converted.csv', 'uefa_2022_converted.csv']

        # Define the columns for the table
        columns = """
            stage VARCHAR, 
            date DATE,
            pens BOOLEAN,
            pens_home_score BOOLEAN,
            pens_away_score BOOLEAN,
            team_name_home VARCHAR,
            team_name_away VARCHAR,
            team_home_score INT,
            team_away_score INT,
            possession_home FLOAT,
            possession_away FLOAT,
            total_shots_home INT,
            total_shots_away INT,
            shots_on_target_home INT,
            shots_on_target_away INT,
            duels_won_home FLOAT,
            duels_won_away FLOAT,
            prediction_team_home_win FLOAT,
            prediction_draw FLOAT,
            prediction_team_away_win FLOAT,
            location VARCHAR       
        """

        for table_name in table_names:
            cur.execute(f"CREATE OR REPLACE TABLE {table_name} ({columns});")

        for table_name, csv_file_name in zip(table_names, csv_file_names):
            cur.execute(f"""
                COPY INTO {table_name}
                FROM @STAGING_AREA/{csv_file_name}
                FILE_FORMAT = (FORMAT_NAME = 'csv_data_format');
            """)

        for table_name in table_names:
            cur.execute(f"SELECT * FROM {table_name} LIMIT 5;")
            result = cur.fetchall()  # Use the cursor to fetch results
            print(f"Data from {table_name}:")
            for row in result:
                print(row)
    except Exception as e:
        print(f"Error loading data: {e}")

if __name__ == "__main__":
    conn = connect()
    cur = conn.cursor()
    if cur:
        load_data(cur)
    cur.close()  # Ensure you close the cursor
    conn.close()  # Close the connection as well
