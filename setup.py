import sql_agent as sql
import os
#create file
f= open("database.db","w+")
#create a data_base
sql_ag = sql.sql_data('database.db','database')
try:
    sql_ag.create_db()
except:
    print('The database is already created.')

