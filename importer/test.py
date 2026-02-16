# File to test the dynamic importer function
from  db_importer import db_importer

file_path =  input('Enter the path to the CSV/Excel file>>> ')
db_name = input('Enter your Database name>>> ')
table_name = input('Enter your table name>>> ')
username = input('Enter your username>>> ')
password = input('Enter your password>>> ')

result = db_importer(file_path=file_path, db_name=db_name, table_name=table_name, username=username, password=password)
print(result)

