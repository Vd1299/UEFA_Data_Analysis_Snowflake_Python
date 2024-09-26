import pandas as pd
from dateutil import parser
import os

def convert_date(date_str):
    try:
        return parser.parse(date_str).strftime('%Y-%m-%d')
    except ValueError:
        return None

csv_files = ['uefa_2020.csv', 'uefa_2021.csv', 'uefa_2022.csv']

percentage_columns = ['POSSESSION_HOME', 'POSSESSION_AWAY', 'DUELS_WON_HOME', 'DUELS_WON_AWAY', 'PREDICTION_TEAM_HOME_WIN', 'PREDICTION_DRAW', 'PREDICTION_TEAM_AWAY_WIN']

for csv_file in csv_files:
    try:
        df = pd.read_csv(csv_file, encoding='latin1')
        
        df['DATE'] = df['DATE'].apply(convert_date)
        
        for col in percentage_columns:
            if col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].str.rstrip('%').astype(float) / 100
                elif df[col].dtype in ['int64', 'float64']:
                    df[col] = df[col] / 100

        base_name = os.path.splitext(csv_file)[0]
        df.to_csv(f'{base_name}_converted.csv', index=False)
        
        print(f"Processed {csv_file} successfully.")
    except FileNotFoundError:
        print(f"File not found: {csv_file}")
    except Exception as e:
        print(f"An error occurred while processing {csv_file}: {e}")
