import pandas as pd
import psycopg2
import shutil
import os

try:
    # read the connection parameters
    # params = Config()
    # connect to the PostgreSQL server
    # conn = psycopg2.connect(**params)
    conn = psycopg2.connect('dbname=files')
    SQL_Query = pd.read_sql_query("""SELECT fullpathtooriginalfile, originalfileextension, createdyear, createdmonth,\
    newfilename, appendthisstring FROM data.data where appendthisstring = '0000' and originalfileextension = 'jpg';""", conn)
    conn.commit()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()


df = pd.DataFrame(SQL_Query)

df['newfullfilename'] = '/Volumes/Sync2Google/NewMedia/Pictures/' +\
                      df['createdyear'] + '/' + df['createdmonth'] + '/' + df['newfilename']

df.head(25)

print(df)

for index, row in df.iterrows():
    print(row['fullpathtooriginalfile'], row['newfullfilename'])
    try:
        shutil.copy(row['fullpathtooriginalfile'], row['newfullfilename'])
    except IOError as io_err:
        os.makedirs(os.path.dirname(row['newfullfilename']))
        shutil.copy(row['fullpathtooriginalfile'], row['newfullfilename'])



