
appendthisstring = "0000"
appendthisnumber = 0

conn = None
try:
    # read database configuration

    # connect to the PostgreSQL database
    conn = psycopg2.connect('dbname=files')
    # create a new cursor
    cur = conn.cursor()
    # execute the INSERT statement
    cur.execute(sql, [newfilename])
    results = cur.fetchone()
    # result = cur.execute("SELECT count(*) FROM data WHERE newfilename = '%s'"%str(newfilename))
    if results[0] > 0:
        appendthisnumber = random.randint(1, 9999)
        appendthisstring = str(appendthisnumber).zfill(4)
    # commit the changes to the database
    conn.commit()
    # close communication with the database
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()

newfilename = createddateid + "_" + appendthisstring + "." + originalfileextension

print(newfilename)

sql = """INSERT INTO data.data(fullpathtooriginalfile,containingfolder,
originalfilename,originalfileextension,lastmodifieddateid,createddateid,createdyear,createdmonth,newfilename)
VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

conn = None
try:
    # read database configuration

    # connect to the PostgreSQL database
    conn = psycopg2.connect('dbname=files')
    # create a new cursor
    cur = conn.cursor()
    # execute the INSERT statement
    cur.execute(sql, (
        fullpathtooriginalfile, containingfolder, originalfilename, originalfileextension, lastmodifieddateid,
        createddateid, createdyear, createdmonth, newfilename))
    # commit the changes to the database
    conn.commit()
    # close communication with the database
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
