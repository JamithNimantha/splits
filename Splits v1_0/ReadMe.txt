Files
##############################################################################################
1 - entry.py
    Entry object class. converts data into suitable form upon providing required params
2 - logger.py
    event logger
3 - postgreSQL.py
    postgreSQL general class
4 - sql_client.py
    sql_client class customised to this project. Inherits postgreSql.
5 - tools.py
    required extra function
6 - splits.py
    main file. 
    generates date according to condition, 
    generates links
    fetches page data and parses it.
    passes the row data into Entry object to format it and save it db.
##############################################################################################