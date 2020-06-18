import pandas as pd
import psycopg2

from sqlalchemy import create_engine
engine = create_engine('postgresql://pythonuser:pythonuser@localhost:5432/data')
#db = create_engine(db_string)

conn = None
command = ("DROP TABLE IF EXISTS data.folderpathsjpg;")

try:
    # read the connection parameters
    # params = Config()
    # connect to the PostgreSQL server
    # conn = psycopg2.connect(**params)
    conn = psycopg2.connect('dbname=data')
    cur = conn.cursor()
    cur.execute(command)
    # close communication with the PostgreSQL database server
    cur.close()
    # commit the changes
    conn.commit()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()

command = ("""SELECT fullpathtocontainingfolder,count(*) as PictCount INTO data.folderpathsjpg
FROM data.data
where originalfileextension = 'jpg'
group by fullpathtocontainingfolder
order by 2 desc;""")

try:
    # read the connection parameters
    # params = Config()
    # connect to the PostgreSQL server
    # conn = psycopg2.connect(**params)
    conn = psycopg2.connect('dbname=files')
    cur = conn.cursor()
    # create table one by one
    cur.execute(command)
    # close communication with the PostgreSQL database server
    cur.close()
    # commit the changes
    conn.commit()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()

try:
    # read the connection parameters
    # params = Config()
    # connect to the PostgreSQL server
    # conn = psycopg2.connect(**params)
    conn = psycopg2.connect('dbname=files')
    SQL_Query = pd.read_sql_query("""SELECT fullpathtocontainingfolder from data.folderpathsjpg""", conn)
    conn.commit()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()


df = pd.DataFrame(SQL_Query, columns=['fullpathtocontainingfolder'])

df1 = df.fullpathtocontainingfolder.apply(lambda x: pd.Series(str(x).split("/")))

df2 = pd.DataFrame()
df2 = pd.merge(df, df1, left_index=True, right_index=True)

print(df2)

melteddf = pd.DataFrame()
cols = df1.columns
print(cols)

#cols.remove('fullpathtocontainingfolder')
melteddf = pd.melt(df2, id_vars=['fullpathtocontainingfolder'], value_vars=cols)
print(melteddf)

melteddf.to_sql('pathkeywords', schema='data', con=engine, if_exists='replace')


