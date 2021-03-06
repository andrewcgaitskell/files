import os, time
import datetime
import psycopg2
# from config import Config
import random

# conn = psycopg2.connect('dbname=files')
# cur = conn.cursor()

conn = None
command = ("DROP TABLE IF EXISTS data.data;")

try:
    # read the connection parameters
    # params = Config()
    # connect to the PostgreSQL server
    # conn = psycopg2.connect(**params)
    conn = psycopg2.connect('dbname=files')
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


command = ("""CREATE TABLE data.data (
    fullpathtooriginalfile VARCHAR(255),
    fullpathtocontainingfolder VARCHAR(1000),
    containingfolder VARCHAR(255),
    originalfilename VARCHAR(255),
    originalfileextension VARCHAR(255),
    createddateid VARCHAR(255),
    createdyear VARCHAR(255),
    createdmonth VARCHAR(255),
    newfilename VARCHAR(500),
    appendthisstring VARCHAR(500));""");

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



def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


#for file in files("."):
#    print(file);


# def getListOfFiles(dirName):
# create a list of file and sub directories
# names in the given directory
# listOfFile = os.listdir(dirName)
# allFiles = list()
# Iterate over all the entries
# for entry in listOfFile:
# Create full path
# fullPath = os.path.join(dirName, entry)
# If entry is a directory then get the list of files in this directory
# if os.path.isdir(fullPath):
#     allFiles = allFiles + getListOfFiles(fullPath)
# else:
#     allFiles.append(fullPath)

# return allFiles


def get_information(directory):
    file_list = []
    for i in os.listdir(directory):
        try:
            a = os.stat(os.path.join(directory, i))
        except Exception:
            pass  # or you could use 'continue'

        fullpathtooriginalfile = os.path.join(directory, i)
        fullpathtocontainingfolder = directory
        # print(b)
        if os.path.isdir(fullpathtooriginalfile):
            get_information(fullpathtooriginalfile)
        fullfilename = i
        if fullfilename[0] != ".":
            foldersaslist = fullpathtooriginalfile.split("/")
            foldercount = len(foldersaslist)
            containingfolder = foldersaslist[foldercount - 2]
            justfilenamesplit = fullfilename.split(".")
            try:
                originalfileextension = justfilenamesplit[1]
            except:
                originalfileextension = ""
            originalfilename = justfilenamesplit[0]
            # lastmodifieddate = time.ctime(a.st_atime)
            # createddate = time.ctime(a.st_ctime)
            # lastmodifieddatetuple = time.gmtime(a.st_atime)
            # lastmodifieddateiso = time.strftime("%Y-%m-%dT%H:%M:%S", lastmodifieddatetuple)
            # lastmodifieddateid = time.strftime("%Y%m%d%H%M%S", lastmodifieddatetuple)
            createddatetuple = time.gmtime(a.st_birthtime)
            createddateiso = time.strftime("%Y-%m-%dT%H:%M:%S", createddatetuple)
            # print("Created: %s" % time.ctime(os.path.getctime("test.txt")))
            # createddatetime = time.ctime(os.path.getctime(fullpathtooriginalfile))
            # createddatetime = time.gmtime(a.st_birthtime)
            print(createddateiso)
            # createddatetuple = datetime.timetuple(createddatetime)
            # print(createddatetuple)
            createddateid = time.strftime("%Y%m%d%H%M%S", createddatetuple)
            createdyear = createddateid[0:4]
            createdmonth = createddateid[0:6]
            newfilename = originalfilename + "_" + createddateid + "_" + "0000" + "." + originalfileextension
            file_list.append(
                [fullpathtooriginalfile, fullpathtocontainingfolder, containingfolder, originalfilename, originalfileextension,
                 createddateid, createdyear, createdmonth, newfilename, "0000"])

            sql = "SELECT count(*) from data.data WHERE newfilename = %s"
            # result = cur.execute("SELECT * FROM users WHERE username = '%s'"%str(username))

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

            newfilename = originalfilename + "_" + createddateid + "_" + appendthisstring + "." + originalfileextension

            print(newfilename)

            sql = """INSERT INTO data.data(fullpathtooriginalfile,fullpathtocontainingfolder,containingfolder,
            originalfilename,originalfileextension,createddateid,createdyear,createdmonth,newfilename,appendthisstring)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

            conn = None
            try:
                # read database configuration

                # connect to the PostgreSQL database
                conn = psycopg2.connect('dbname=files')
                # create a new cursor
                cur = conn.cursor()
                # execute the INSERT statement
                cur.execute(sql, (
                    fullpathtooriginalfile, fullpathtocontainingfolder, containingfolder, originalfilename, originalfileextension,
                    createddateid, createdyear, createdmonth, newfilename, appendthisstring))
                # commit the changes to the database
                conn.commit()
                # close communication with the database
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()

    return file_list


a = get_information("/Volumes/Sync2Google/Media/Pictures20191017")

print(a)
