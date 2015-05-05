# to delete all the tables constructed

import MySQLdb as mdb
import lxml.html
import warnings
import pprint as pp
import sys

# read prefix from file
f = open ("input.txt")
lines = f.readlines()
prefix = lines[1]

# import parse function to get movie data and dob of person
from parse import getMovie
from parse import getDob

# connect to database and get a cursor
try:
    db = mdb.connect('10.5.18.66', '12CS10008', 'btech12', '12CS10008');
    cursor = db.cursor()

except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)

def delete_from_table(tname):
    sql = "delete from "+ prefix +"_"+ tname;
    print sql
    cursor.execute(sql)
    db.commit()

delete_from_table("m_cast;");
delete_from_table("m_country;");
delete_from_table("m_director;");
delete_from_table("m_producer;");
delete_from_table("m_location;");
delete_from_table("m_language;");
delete_from_table("m_genre;");
delete_from_table("country;");
delete_from_table("location;");
delete_from_table("language;");
delete_from_table("genre;");
delete_from_table("person;");
delete_from_table("movie;");