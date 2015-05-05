import MySQLdb as mdb
import sys
import pprint as pp
import matplotlib.pyplot as plt

import networkx as nx

try:
    db = mdb.connect('10.5.18.66', '12CS10008', 'btech12', '12CS10008');
    cursor = db.cursor()

except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)

def construct_graph_a():
	G=nx.Graph()

	# construct nodes
	sql = "select MID from 12CS10008_Movie";
	cursor.execute(sql);
	rows = cursor.fetchall()
	for row in rows:
		# print row[0]
		G.add_node(row[0])

	# construct edges
	sql = "select a.MID,b.MID from 12CS10008_M_Cast as a inner join 12CS10008_M_Cast as b on a.PID = b.PID where a.MID<b.MID"
	cursor.execute(sql);
	rows = cursor.fetchall()
	# for row in rows:
	# 	print row
	G.add_edges_from(rows)

	# print G.number_of_nodes()
	# print G.number_of_edges()
	return G

def construct_graph_b():
	G=nx.Graph()

	# construct nodes
	sql = "select distinct PID from 12CS10008_M_Cast order by PID";
	cursor.execute(sql);
	rows = cursor.fetchall()
	for row in rows:
		# print row[0]
		G.add_node(row[0])

	# construct edges
	sql = "select a.PID,b.PID from 12CS10008_M_Cast as a inner join 12CS10008_M_Cast as b on a.MID = b.MID where a.PID<b.PID"
	cursor.execute(sql);
	rows = cursor.fetchall()
	# for row in rows:
	# 	print row
	G.add_edges_from(rows)

	# print G.number_of_nodes()
	# print G.number_of_edges()
	return G

if __name__ == '__main__':
	# a
	# G = construct_graph_a()
	# print nx.graph_clique_number(G)

	# b
	G = construct_graph_b()
	length=nx.all_pairs_shortest_path_length(G)
	sql = "create table if not exists 12CS10008_Separation (actor_1 varchar(20), actor_2 varchar(20), separation int, primary key (actor_1, actor_2),"
	sql = sql + "foreign key (actor_1) references 12CS10008_Person(PID), foreign key (actor_2) references 12CS10008_Person(PID) )"
	cursor.execute(sql);

	# config
	commit_window = 1000

	# init
	count = 1
	x=0
	for nodei in sorted(G.nodes()):
		for nodej in sorted(G.nodes()):
			if nodei< nodej:
				try:
					d = length[nodei][nodej]
				except:
					d = -1
				print nodei, nodej, d
				if d>0: print "Yes"
				else: print  "No"
				sql = "insert into 12CS10008_Separation (actor_1, actor_2, separation) "
				sql = sql + "SELECT * FROM (SELECT \""+ nodei +"\",\"" + nodej +"\","+ str(d) +") as tmp "
				sql = sql + "WHERE NOT EXISTS ( SELECT actor_1,actor_2 FROM 12CS10008_Separation WHERE actor_1 =\"" + nodei + "\" and  actor_2 =\"" + nodej + "\" ) LIMIT 1"
				# print sql
				cursor.execute(sql);
				count = count+1
				if count ==commit_window:
					print x
					x=x+1
					db.commit()
					count=0


	db.commit()
	# nx.draw(G)
	# plt.show()