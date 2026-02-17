# Dynamic-Data-Importer
A dynamic python pipeline for importing CSV and Excel files into a database with validation and schema handling. This dynamic data importer can essentially import most CSV and Excel files into a mysql database. To use/test the project run the test file:
```bash
test.py
```
# NOTE: In this project is included a sample_table.py file which you can run to create a database and table for test. Along with it are sample csv and excel files which you can use to test. This is to make testing of the project easier.
# Should you decide to use a different mysql database and excel/csv file, that is also totally fine.

 The flow of this project is explained below:

1. # THE DATABASE CONNECTION
The database connection is handled in the database.py file. This file contains two functions:
```bash
a. db_connect(): This function establishes the connection to the database while taking in arguments. These arguments include the database name, the username and the password respectively.

b. db_close(): This function handles the closing of the database connection. It is called once the excel/csv file has been imported into the database. It takes in one argument i.e. conn. This is the connection variable used in closing the database connection.
```

2. # Importing of the Excel/CSV file into the mysql database
This operation is handled in the db_importer.py file. Within this file is the db_importer() function. This function accepts a number of arguments. These arguments include: file path, database name, table name, username and password respectively. The db_connect() and db_close() functions are called within this function and the appropriate arguments are passed to them. 
The db_importer() function handles the following operations:
```bash
1. Loading of the excel or csv file into a DataFrame
2. Retrieving columns from the DataFrame and the Database
3. Checking for missing columns and returning an error message if a missing column is detected.
4. Checking for extra columns and returning a warning message and then adjusting the loaded DataFrame to match that of the database columns
5. Column Validation. This validation involves null checks, default checks, key type constraints and data type mismatches
6. Importing of the clean DataFrame into the mysql database using the "to_sql()" pandas method
```

# It is important to note that during the data type mismatch check, the dynamic check was done in such a way that columns that are expected to be integers are checked exclusively. This is due to the fact that there is a possibility that an integer column could allow for null values. 

# You may wonder why this possibility was taken into consideration. Well, the reason for this is that when excel or csv files containing null values are loaded into a DataFrame. The integer columns containing the null values are casted into a float datatype by pandas. This is due to the fact that a column in a DataFrame is expected to be homogenous and null values in a dataframe are essentially stored internally as float (np.nan).

# This issue needed to be addressed as actual integer columns could be mistaken for float due to having a null value. Hence the appropriate approach was taken. 

# The data type mismatch check hence becomes fully dynamic and functional as it responds to multiple situations.

```bash
A file called "test.py" was also created. This is to enable one to test the project

The project can be easily tweaked to fit your needs. For example, if you wanted to employ this functionality to a frontend, it is very possible to do so.
```