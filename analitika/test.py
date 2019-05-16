#imports
import analitics as an
import sql_agent as sql

sql_ag = sql.sql_data('test.db','test')
try:
    sql_ag.create_db()
except:
    pass
f= open("data_csv/default_dataset.csv")
sql.import_ride(sql_ag, f)
sql_ag.con.commit()



            
        

    
        

