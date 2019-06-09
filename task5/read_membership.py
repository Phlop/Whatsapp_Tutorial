import os;
import sys,sqlite3
import time,datetime;
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,random;
reload(sys)
sys.setdefaultencoding('utf8')

file_names = [sys.argv[1]]; # folder containin the databases.

def getMembership(files):
	out = open("group_membership.csv","w");
	out.write("group_id\tsender_id\tis_admin\n");
	for infile in files:
		print >> sys.stderr, infile;
		conn = sqlite3.connect(infile);
		conn.text_factory = str
		c = conn.cursor();
		c.execute("select gjid,jid,admin from group_participants");
		all_rows = c.fetchall()

		for row in all_rows:
			if(row[1]!=""): #uncomment to print group membership data
				out.write(row[0] + "\t" + row[1] + "\t" + str(row[2]) + "\n");
	out.close();


def main():

    print >> sys.stderr, "Getting groups membership";
    getMembership(file_names);


if __name__ == '__main__':
	main()
