import os;
import sys,sqlite3
import time,datetime;
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,json,random;
reload(sys)
sys.setdefaultencoding('utf8')

file_names = [sys.argv[1]] ; 

def getMessages(files):
	table_name = "messages";
	count = 0;
	dict_group_database = {};
	out = open("messages.csv","w");
	out.write("group_id\tsender_id\tdata\ttimestamp\tmedia_url\tmedia_mime_type\tmedia_size\trecipient_count\tforwarded\n");
	for infile in files:
		print >> sys.stderr, infile;
		conn = sqlite3.connect(infile);
		conn.text_factory = str
		c = conn.cursor();
		c.execute("select key_remote_jid,remote_resource,data,timestamp,media_url,media_mime_type,media_size,recipient_count,forwarded,status from messages");
		all_rows = c.fetchall()

		for row in all_rows:
			if(row[0] is not None):
				dict_group_database[row[0]] = infile;
				groupid = row[0];
				sender_id = row[1];
				data = row[2];
				timestamp = row[3];
				media_url = row[4];
				media_mime_type = row[5];
				media_size = row[6];
				recipient_count = row[7];
				forwarded = row[8];
				status = row[9];
				if(data is not None):
					data = data.encode("utf-8").replace("\n"," ").replace("\t"," ");
				else:
					data = "";
				if(row[9]==6): # filter non textual messages (events)
					continue;
				try:
#				for i in range(1,2):
					out.write(str(groupid).encode("utf-8") + "\t" + str(sender_id).encode("utf-8") + "\t" + str(data).encode("utf-8") + "\t" + str(timestamp).encode("utf-8") + "\t" + str(media_url).encode("utf-8") + "\t" + str(media_mime_type).encode("utf-8") + "\t" + str(media_size).encode("utf-8") + "\t" + str(recipient_count).encode("utf-8") + "\t" + str(forwarded).encode("utf-8") + "\n");
				except:
					count += 1;
					continue;
#		break;

	out.close();

	out1 = open("groupid_database_mapping.txt","w");
	for keys in dict_group_database.keys():
		out1.write(keys + "\t" + dict_group_database[keys] + "\n");
	out1.close();


def main():
	print >> sys.stderr, "getting messages";
	getMessages(file_names);

if __name__ == '__main__':
	main()
