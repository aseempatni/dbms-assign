import MySQLdb as mdb
import lxml.html
import warnings
import pprint as pp
import sys

# import parse function to get movie data
from parse import getMovie

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


def ptable(name):
    sql = "select * from "+prefix+ "_" + name
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print row

# add data for movie with id to db
def add_all(id):

    # with warnings.catch_warnings():
    #     warnings.simplefilter('ignore')
    #     sql = "DROP TABLE IF EXISTS "+prefix+"_m_producer"
    #     print sql
    #     cursor.execute(sql)
    #     sql = "DROP TABLE IF EXISTS "+prefix+"_m_director"

    # get movie data
    print "Getting data"
    data = getMovie(id)
    # pp.pprint (data)
    print "Adding "+data['title'] +" to db"
    add_movie(data)
    # ptable("movie")
    add_cast(data)


if __name__ == '__main__':
    id = sys.argv[1]
    add_all(id)
    if db:
        db.close()