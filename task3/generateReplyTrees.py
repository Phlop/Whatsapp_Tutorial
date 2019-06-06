# script to generate a reply tree of who replies to whom in a group.

import sys;
import re,sqlite3
import time,datetime;
import networkx as nx;
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,json,random;
reload(sys)
sys.setdefaultencoding('utf8')
import matplotlib;
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#f2 = open("namobharat_groups.txt");
f2 = open("ftnbjp_groups.txt");
lines2 = f2.readlines();
dict_ftnbjp = {};

for line in lines2:
	line = line.strip();
	line_split =  line.split("\t");
	dict_ftnbjp[line_split[0]] = 1;

sqlite_file = sys.argv[1];#"/mnt/kiran/whatsapp/databases_backup/micromax/3_12_2018.db";
conn = sqlite3.connect(sqlite_file);
conn.text_factory = str
c = conn.cursor();

command = "SELECT messages.key_remote_jid, messages.remote_resource, messages.key_id, messages_quotes.key_id, messages_quotes.remote_resource from messages inner join messages_quotes on messages_quotes._id = messages.quoted_row_id;"

c.execute(command);
all_rows = c.fetchall()
dict_mapping = {};
count = 0;

G = nx.DiGraph();

for row in all_rows:
	group = row[0];
	replier = row[1].replace("@s.whatsapp.net","");
	replier_message_id = row[2];
	replying_to_message_id = row[3];
	replying_to = row[4].replace("@s.whatsapp.net","");
#	print group, replier, replying_to;
#	continue;
#	if(group!="916380599108-1517246583@g.us"):
#		continue;
	if(group not in dict_ftnbjp):
		continue;
	if(replying_to_message_id not in dict_mapping):
		dict_mapping[replying_to_message_id] = count;
		count += 1;
	if(replier_message_id not in dict_mapping):
		dict_mapping[replier_message_id] = count;
		count += 1;
	
#	G.add_node(replying_to);
#	G.add_node(replier);
#	G.add_edge(replying_to,replier);
	G.add_node(dict_mapping[replying_to_message_id]);
	G.add_node(dict_mapping[replier_message_id]);
	G.add_edge(dict_mapping[replying_to_message_id],dict_mapping[replier_message_id]);

out = open("reply_mapping.txt","w");
for keys in dict_mapping.keys():
	out.write(keys + "\t" + str(dict_mapping[keys]) + "\n");
out.close();
nx.drawing.nx_pydot.write_dot(G,'/home/cloud-user/Dropbox/tmp/test.dot');
print len(G.nodes()), len(G.edges());
#nx.write_edgelist(G,'/home/cloud-user/Dropbox/tmp/1.csv');
#[len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]
components = nx.weakly_connected_components(G);
x = [];
for component in components:
	if(len(component)<3):
		continue;
	x.append(len(component));
#	print nx.dag_longest_path(component);
plt.hist(x,20);
plt.xlabel("Num nodes");
plt.ylabel("Frequency");
plt.savefig("/home/cloud-user/Dropbox/tmp/whatsapp_analysis/reply_nodes.pdf");
plt.close();


