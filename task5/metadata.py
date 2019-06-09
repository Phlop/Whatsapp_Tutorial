import os,glob;
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

file_name = sys.argv[1]; # folder containin the databases.


def main():
   
    con = sqlite3.connect(file_name)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all = cursor.fetchall()
    print ("Getting table names")
    for table in all:
        print str(table)
	
    
    print ("Getting columns names from a table")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sqlite_master WHERE name = 'messages';")
    print(cursor.fetchall())
	



if __name__ == '__main__':
	main()