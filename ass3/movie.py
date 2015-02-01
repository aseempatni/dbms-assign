import MySQLdb as mdb
import lxml.html
import warnings
import pprint as pp
import sys

# this script adds the data to the database

# import parse function to get movie data and dob of person
from parse import getMovie
from parse import getDob

# connect to database and get a cursor
try:
    db = mdb.connect('10.5.18.68', '12CS10008', 'btech12', '12CS10008');
    cursor = db.cursor()

except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)

# read prefix from file
f = open ("input.txt")
lines = f.readlines()
prefix = lines[1]

# config
addDob = False


# add to movie table
def add_movie(data) :

#     INSERT INTO  12CS10008_movie(MID, title, year, rating, num_votes)
# SELECT * FROM (SELECT "tt1375666","Inception",2010,8.8,1145641) AS tmp
# WHERE NOT EXISTS (
#     SELECT MID FROM 12CS10008_movie WHERE MID = 'tt1375666'
# ) LIMIT 1;
    sql = ""
    sql = sql + "INSERT INTO " +prefix+"_movie(MID, title, year, rating, num_votes) "
    sql = sql + "SELECT * FROM (SELECT " + "\""+data['MID']+"\",\""+data['title']+"\","+ data['year']+","+ data['rating']+","+data['num_votes'].replace(',',   '') +" ) as tmp "
    sql = sql + "WHERE NOT EXISTS ( SELECT MID FROM  " + prefix+"_movie WHERE MID =\"" + data['MID'] + "\" ) LIMIT 1"
    # print sql
    cursor.execute(sql)
    db.commit()

def add_cast(data):
    for i in range(len(data['cast'])):
        if addDob==True:
            dob = getDob(data['cast'][i][0])
            # add cast to person
            sql = ""
            sql = sql + "INSERT INTO " +prefix+"_person(PID, name, DOB) "
            sql = sql + "SELECT * FROM (SELECT " + "\""+data['cast'][i][0]+"\",\""+data['cast'][i][1]+"\"" +", "+ dob +") as tmp "
            sql = sql + "WHERE NOT EXISTS ( SELECT PID FROM  " + prefix+"_person WHERE PID =\"" + data['cast'][i][0] + "\" ) LIMIT 1"
            # print sql
            cursor.execute(sql)
            db.commit()
        else:
            # add cast to person
            sql = ""
            sql = sql + "INSERT INTO " +prefix+"_person(PID, name) "
            sql = sql + "SELECT * FROM (SELECT " + "\""+data['cast'][i][0]+"\",\""+data['cast'][i][1]+"\"" +") as tmp "
            sql = sql + "WHERE NOT EXISTS ( SELECT PID FROM  " + prefix+"_person WHERE PID =\"" + data['cast'][i][0] + "\" ) LIMIT 1"
            # print sql
            cursor.execute(sql)
            db.commit()

        # add the mapping
        sql = ""
        sql = sql + "INSERT INTO " +prefix+"_m_cast(MID, PID) "
        sql = sql + "SELECT * FROM (SELECT " + "\""+data['MID']+"\",\""+data['cast'][i][0]+"\"" +") as tmp "
        sql = sql + "WHERE NOT EXISTS ( SELECT MID, PID FROM  " + prefix+"_m_cast WHERE MID =\"" + data['MID'] + "\" AND PID =\"" + data['cast'][i][0] + "\" ) LIMIT 1"
        # print sql
        cursor.execute(sql)
        db.commit()

def add_producer(data):
    for i in range(len(data['producer'])):

        # add producer to person
        sql = ""
        sql = sql + "INSERT INTO " +prefix+"_person(PID, name) "
        sql = sql + "SELECT * FROM (SELECT " + "\""+data['producer'][i][0]+"\",\""+data['producer'][i][1]+"\"" +") as tmp "
        sql = sql + "WHERE NOT EXISTS ( SELECT PID FROM  " + prefix+"_person WHERE PID =\"" + data['producer'][i][0] + "\" ) LIMIT 1"
        # print sql
        cursor.execute(sql)
        db.commit()

        # add the mapping
        sql = ""
        sql = sql + "INSERT INTO " +prefix+"_m_producer(MID, PID) "
        sql = sql + "SELECT * FROM (SELECT " + "\""+data['MID']+"\",\""+data['producer'][i][0]+"\"" +") as tmp "
        sql = sql + "WHERE NOT EXISTS ( SELECT MID, PID FROM  " + prefix+"_m_producer WHERE MID =\"" + data['MID'] + "\" AND PID =\"" + data['producer'][i][0] + "\" ) LIMIT 1"
        # print sql
        cursor.execute(sql)
        db.commit()

def add_director (data):
    # add director to map and person
    sql = ""
    sql = sql + "INSERT INTO " +prefix+"_person(PID, name) "
    sql = sql + "SELECT * FROM (SELECT " + "\""+data['DID']+"\",\""+data['director']+"\"" +") as tmp "
    sql = sql + "WHERE NOT EXISTS ( SELECT PID FROM  " + prefix+"_person WHERE PID =\"" + data['DID']+ "\" ) LIMIT 1"
    cursor.execute(sql)
    db.commit()    
    sql = ""
    sql = sql + "INSERT INTO " +prefix+"_m_director(MID, PID) "
    sql = sql + "SELECT * FROM (SELECT " + "\""+data['MID']+"\",\""+data['DID']+"\"" +") as tmp "
    sql = sql + "WHERE NOT EXISTS ( SELECT MID, PID FROM  " + prefix+"_m_director WHERE MID =\"" + data['MID'] + "\" AND PID =\"" + data['DID'] + "\" ) LIMIT 1"
    cursor.execute(sql)
    db.commit()    

def add_genre (data):
    for i in range(len(data['genre'])):
        # add genre to genre and m_genre
        sql = ""
        sql = sql + "INSERT INTO " +prefix+"_genre(name) "
        sql = sql + "SELECT * FROM (SELECT " + "\""+data['genre'][i]+"\") as tmp "
        sql = sql + "WHERE NOT EXISTS ( SELECT name FROM  " + prefix+"_genre WHERE name =\"" + data['genre'][i]+ "\" ) LIMIT 1"
        cursor.execute(sql)
        db.commit()
        sql = "SELECT GID FROM "+prefix+"_genre" + " WHERE name = \"" + data['genre'][i] + "\""
        cursor.execute(sql)
        GID = str(cursor.fetchall()[0][0])
        # print GID
        sql = ""
        sql = sql + "INSERT INTO " +prefix+"_m_genre(MID, GID) "
        sql = sql + "SELECT * FROM (SELECT " + "\""+data['MID']+"\","+ GID +") as tmp "
        sql = sql + "WHERE NOT EXISTS ( SELECT MID, GID FROM  " + prefix+"_m_genre WHERE MID =\"" + data['MID'] + "\" AND GID =" + GID + " ) LIMIT 1"
        # print sql
        cursor.execute(sql)
        db.commit() 

def add_country (data):
    for i in range(len(data['country'])):
        # add country to country and m_country
        sql = ""
        sql = sql + "INSERT INTO " +prefix+"_country(name) "
        sql = sql + "SELECT * FROM (SELECT " + "\""+data['country'][i]+"\") as tmp "
        sql = sql + "WHERE NOT EXISTS ( SELECT name FROM  " + prefix+"_country WHERE name =\"" + data['country'][i]+ "\" ) LIMIT 1"
        cursor.execute(sql)
        db.commit()
        sql = "SELECT CID FROM "+prefix+"_country" + " WHERE name = \"" + data['country'][i] + "\""
        cursor.execute(sql)
        CID = str(cursor.fetchall()[0][0])
        # print CID
        sql = ""
        sql = sql + "INSERT INTO " +prefix+"_m_country(MID, CID) "
        sql = sql + "SELECT * FROM (SELECT " + "\""+data['MID']+"\","+ CID +") as tmp "
        sql = sql + "WHERE NOT EXISTS ( SELECT MID, CID FROM  " + prefix+"_m_country WHERE MID =\"" + data['MID'] + "\" AND CID =" + CID + " ) LIMIT 1"
        # print sql
        cursor.execute(sql)
        db.commit() 

def add_language (data):
    for i in range(len(data['language'])):
        # add language to language and m_language
        sql = ""
        sql = sql + "INSERT INTO " +prefix+"_language(name) "
        sql = sql + "SELECT * FROM (SELECT " + "\""+data['language'][i]+"\") as tmp "
        sql = sql + "WHERE NOT EXISTS ( SELECT name FROM  " + prefix+"_language WHERE name =\"" + data['language'][i]+ "\" ) LIMIT 1"
        cursor.execute(sql)
        db.commit()
        sql = "SELECT LAID FROM "+prefix+"_language" + " WHERE name = \"" + data['language'][i] + "\""
        cursor.execute(sql)
        LAID = str(cursor.fetchall()[0][0])
        # print LAID
        sql = ""
        sql = sql + "INSERT INTO " +prefix+"_m_language(MID, LAID) "
        sql = sql + "SELECT * FROM (SELECT " + "\""+data['MID']+"\","+ LAID +") as tmp "
        sql = sql + "WHERE NOT EXISTS ( SELECT MID, LAID FROM  " + prefix+"_m_language WHERE MID =\"" + data['MID'] + "\" AND LAID =" + LAID + " ) LIMIT 1"
        # print sql
        cursor.execute(sql)
        db.commit() 

def add_location (data):
    for i in range(len(data['location'])):
        # add location to location and m_location
        sql = ""
        sql = sql + "INSERT INTO " +prefix+"_location(name) "
        sql = sql + "SELECT * FROM (SELECT " + "\""+data['location'][i]+"\") as tmp "
        sql = sql + "WHERE NOT EXISTS ( SELECT name FROM  " + prefix+"_location WHERE name =\"" + data['location'][i]+ "\" ) LIMIT 1"
        cursor.execute(sql)
        db.commit()
        sql = "SELECT LID FROM "+prefix+"_location" + " WHERE name = \"" + data['location'][i] + "\""
        cursor.execute(sql)
        LID = str(cursor.fetchall()[0][0])
        # print LID
        sql = ""
        sql = sql + "INSERT INTO " +prefix+"_m_location(MID, LID) "
        sql = sql + "SELECT * FROM (SELECT " + "\""+data['MID']+"\","+ LID +") as tmp "
        sql = sql + "WHERE NOT EXISTS ( SELECT MID, LID FROM  " + prefix+"_m_location WHERE MID =\"" + data['MID'] + "\" AND LID =" + LID + " ) LIMIT 1"
        # print sql
        cursor.execute(sql)
        db.commit() 

def ptable(name):
    sql = "select * from "+prefix+ "_" + name
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print row

# add data for movie with id to db
def add_all(id):
    # get movie data
    print "Getting data"
    data = getMovie(id)
    # pp.pprint (data)

    print "Adding "+data['title'] +" to db"
    add_movie(data)
    add_cast(data)
    add_director(data)
    add_genre(data)
    add_country(data)
    add_language(data)
    add_location(data)
    add_producer(data)

if __name__ == '__main__':
    id = sys.argv[1]
    add_all(id)
    if db:
        db.close()