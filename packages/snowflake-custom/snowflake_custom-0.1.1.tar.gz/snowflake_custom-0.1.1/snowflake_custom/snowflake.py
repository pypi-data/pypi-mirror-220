import snowflake.connector as sf
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

class get_sf_data:
    def __init__(self,user,password,account,warehouse,role,query_path):
        cnn = sf.connect(
          user = user,
          password = password,
          account = account,
          warehouse = warehouse,
          role = role)
        
        with open(query_path,'r') as f:
            self.query = f.read()

        self.df = pd.read_sql(self.query,cnn)

        cnn.close()

class load_to_sf:
    def __init__(self,user,password,account,warehouse,role,database,schema,table,data):
        cnn = sf.connect(
          user = user,
          password = password,
          account = account,
          warehouse = warehouse,
          database = database,
          schema = schema,
          role = role)
        
        sf_cols = []
        sf_tr = []

        data_cols = data.columns

        self.full_table_name = ".".join([database,schema,table])

        for i in range(len(data_cols)):
        #new_value = data_cols[i].lower() #  + ' ' + 'string'
            if data[data_cols[i]].dtype.name in ('int64'):
                new_value = data_cols[i].lower()  + ' ' + 'integer'
                transform = 'nullif(' + data_cols[i].lower() + ',0) as ' + data_cols[i].lower()
            elif data[data_cols[i]].dtype.name in ('float64'):
                new_value = data_cols[i].lower()  + ' ' + 'float'
                transform = 'nullif(' + data_cols[i].lower() + ',0) as ' + data_cols[i].lower() 
            elif data[data_cols[i]].dtype.name in ('date'):
                new_value = data_cols[i].lower()  + ' ' + 'date'
                transform = 'nullif(' + data_cols[i].lower() + ',\'nan\') as ' + data_cols[i].lower()
            else: 
                new_value = data_cols[i].lower()  + ' ' + 'string'
                transform = 'nullif(' + data_cols[i].lower() + ',\'nan\') as ' + data_cols[i].lower()
            sf_cols.append(new_value)
            sf_tr.append(transform)

        self.query = "\n,".join(sf_cols)

        self.query_nulls = "select\n" + "\n,".join(sf_tr) + "\nfrom\n" + self.full_table_name

        cnn.cursor().execute(
            "CREATE SCHEMA IF NOT EXISTS " + ".".join([database,schema]) 
        )

        cnn.cursor().execute(
            "CREATE OR REPLACE TABLE " + self.full_table_name + "("  + self.query + ")"
        )

        success, nchunks, nrows, _ = write_pandas(cnn, data, table, database, schema, on_error = "CONTINUE",quote_identifiers=False)
        print(str(success) + ', ' + str(nchunks) + ', ' + str(nrows))

        cnn.cursor().execute(
            "CREATE OR REPLACE TABLE " + self.full_table_name + " as\n" + self.query_nulls
        )

        cnn.close()
