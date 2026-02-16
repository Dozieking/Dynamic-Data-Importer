import pandas as pd
from database import db_connect, db_close
from sqlalchemy import create_engine
import datetime


def db_importer(file_path, db_name, table_name, username, password):
    # function to dynamically  import excel/csv files into a database table

    # Load the file into a DataFrame
    try:
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path).convert_dtypes()
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path).convert_dtypes()

    except Exception as e:
        return (f"Error loading file: {e}")

    # Retrieve the columns from the DataFrame
    columns = [col.strip() for col in df.columns]

    
    conn, cursor =  db_connect(db_name, username, password)
    cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
    cols_info = cursor.fetchall()

    # Retrive the column names from the database table
    db_cols = [col[0] for col in cols_info if col[0]!='id' and col[5] !='auto_increment']

    # Check for missing/extra columns
    missing_cols = [col for col in db_cols if col not in columns]
    extra_cols = [col for col in columns if col not in db_cols]

    if missing_cols:
        return (f"Missing columns in file: {missing_cols}!!!!")
    
    elif extra_cols:
        print (f"Extra columns in file: {extra_cols}!!!")
    
    df = df[db_cols]

    # Column Validation
    for col_name, col_type, is_null, key_type, default, extra_info in cols_info:
        if col_name == 'id' and extra_info == 'auto_increment':
            continue
        
        series = df[col_name]

        # Check for null values in non-nullable columns
        if series.isnull().any() and is_null == 'NO':
            return (f"Column '{col_name}' contains null values but is defined as NOT NULL in the database table.")
        
        # Check for key type constraints        
        if (key_type == 'PRI' or key_type == 'UNI'):
            # Check for null values and duplicates in PRIMARY KEY or UNIQUE KEY columns
            if series.isnull().any():
                return (f"Column '{col_name}' contains null values but is defined as a PRIMARY KEY or UNIQUE KEY in the database table.")
            if series.duplicated().any():
                return (f"Column '{col_name}' has duplicate values but is defined as a PRIMARY KEY or UNIQUE KEY in the database table.")

            # Check for duplicates against the database table
            cursor.execute(f"SELECT `{col_name}` FROM `{table_name}`")
            existing_values = [row[0] for row in cursor.fetchall()]
            if series.isin(existing_values).any():
                return (f"Column '{col_name}' contains values that already exist in the database table, violating the PRIMARY KEY or UNIQUE KEY constraint.")
            
        # Check for data type mismatches
        clean_type = col_type.split('(')[0].lower()
        sql_to_python = {
            'int': int,
            'tinyint': bool if clean_type == 'tinyint' and col_type.startswith('tinyint(1)') else int,
            'smallint': int,
            'mediumint': int,
            'bigint': int,
            'char': str,
            'varchar': str,
            'text': str,
            'mediumtext': str,
            'text': str,
            'tinytext': str,
            'mediumtext': str,
            'longtext': str,
            'enumm': str,
            'set': str,
            'date': datetime.date,
            'datetime': datetime.datetime,
            'timestamp': datetime.datetime,
            'time': datetime.time,
            'year': int,
            'float': float,
            'double': float,
            'decimal': float,
            'numeric': float,
            'bool': bool,
            ' bit': int
        }

        sql_data_type = sql_to_python.get(clean_type, 'Not Found')
        if sql_data_type == 'Not Found':
            return (f"The detected data type of the '{col_name}' column is not defined in the expected data type dictionary.")
        
        if sql_data_type == int:
            if not series.apply(lambda x: isinstance(x, (int,float))).all():
                return (f"Column '{col_name}' contains data type mismatches. Expected data type: {sql_data_type.__name__}.")

            if  not series.apply(lambda x: isinstance(x, sql_data_type)).all() and not series.dropna().apply(lambda x: float(x).is_integer()).all():
                return (f"Column '{col_name}' contains data type mismatches. Expected data type: {sql_data_type.__name__}.")
        else:
            if not series.apply(lambda x: isinstance(x, sql_data_type)).all():
                return (f"Column '{col_name}' contains data type mismatches. Expected data type: {sql_data_type.__name__}.")
        
    # Insert the DataFrame into the database using to_sql
    try:
        engine = create_engine(f'mysql+pymysql://{username}:@localhost/{db_name}')
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        return(f" Successfuly imported {len(df)} rows into {table_name} ")

    except Exception as e:
        return (f"Error inserting data into the database: {e}")
    
    finally:
        db_close(conn)
        return(f'''Successfuly imported {len(df)} rows into {table_name} 
Database connection closed''')

        


    


