import os
import sys,re,sqlite3
import time,datetime;
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,json,random;
reload(sys)
sys.setdefaultencoding('utf8')

from urlparse import urlparse
import magic

group_re = re.compile("chat.whatsapp.com/\w+");

sqlite_file = sys.argv[1];#"/mnt/kiran/whatsapp/databases_backup/micromax/3_12_2018.db";
conn = sqlite3.connect(sqlite_file);
conn.text_factory = str
c = conn.cursor();

table_name = "messages";

#c.execute('SELECT data,media_url,media_hash,media_enc_hash,media_wa_type,thumb_image FROM {tn}'. format(tn=table_name))
#c.execute('SELECT key_remote_jid,data,timestamp,origin,forwarded FROM {tn}'. format(tn=table_name))
c.execute("select key_remote_jid,data,timestamp,media_url,media_mime_type,media_size,media_name,remote_resource,recipient_count,forwarded from messages");
#c.execute("select gjid,jid,admin from group_participants");

all_rows = c.fetchall()

"""
for row in all_rows:
	if(row[1] is not None and row[1]!=""):
		print row[0] + "\t" + row[1] + "\t" + str(row[2]);
"""

count = 0;
for row in all_rows:
	forwarded = row[1];
#	print forwarded/1000;
	if(row[0] is not None):
#		print row[3];
#		continue;
#		data = row[1]/1000;
#		if(data>=1543622400 and data<=1544659200):
#			timestamp = datetime.datetime.utcfromtimestamp(data).strftime('%Y-%m-%d %H:%M:%S');
#			try:
#			for i in range(1,2):
		if(row[1] is not None):
			data = row[1].encode("utf-8").replace("\n"," ").replace("\t"," ");
#				else:
#					if(row[3] is None):
#						continue;
		else:
			data = "";
		try:
			print str(row[0]).encode("utf-8") + "\t" + str(data).encode("utf-8") + "\t" + str(row[2]).encode("utf-8") + "\t" + str(row[3]).encode("utf-8") + "\t" + str(row[4]).encode("utf-8") + "\t" + str(row[5]).encode("utf-8") + "\t" + str(row[6]).encode("utf-8") + "\t" + str(row[7]).encode("utf-8") + "\t" + str(row[8]).encode("utf-8") + "\t" + str(row[9]).encode("utf-8");
		except:
			count += 1;
			continue;
#		if(row[0]!="917976551974-1530248391@g.us"):
#			continue;
#		if(row[4]!=""):
#			print row[0].encode("utf-8") + "\t" + str(row[1]) + "\t" + row[2].encode("utf-8");# + "\t" + str(row[3]).encode("utf-8") + "\t" + str(row[4]).encode("utf-8") + "\t" + str(row[5]).encode("utf-8") + "\t" + str(row[6]).encode("utf-8") + "\t" + str(row[7]).encode("utf-8");
#		print row[0] + "\t" + row[1];
#		if(data!=""):
#			print data.replace("\n","").encode("utf-8");#, 
#		groups = re.findall(group_re,data);
#		if(len(groups)>0):			
#			print groups[0],row[2].encode("utf-8");
print >> sys.stderr, count;
