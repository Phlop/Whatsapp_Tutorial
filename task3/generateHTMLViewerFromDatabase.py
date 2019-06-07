import sys;
reload(sys)
import sqlite3;
sys.setdefaultencoding("utf-8")
from operator import itemgetter;
from datetime import datetime;

dict_timeline = {};
dict_groups = {};
html_location = sys.argv[1]; # provide the location of a folder to write the html files to.

db_name = sys.argv[2]; # database name
db_conn = sqlite3.connect(db_name);
cur = db_conn.cursor();
cur.execute("SELECT key_remote_jid,data,timestamp,media_url,media_mime_type,media_size,media_name,remote_resource,recipient_count,forwarded FROM MESSAGES")

lines = []

for i in cur.fetchall():
	lines.append(i);
#print(lines[1:10])

cur.execute("SELECT key_remote_jid,subject FROM chat_list");

temp_dict = {};

for i in cur.fetchall():
	temp_dict[i[0]] = i[1];
#print(temp_dict)

# message_data_8_4.csv
for line in lines:
	line_split = [];
	for val in line:
		if type(val) == type(None):
			line_split.append("")
		else:
			line_split.append(val)
	if(len(line_split)<9):
		continue;
	groupid = line_split[0];
	data = (line_split[1]).encode('utf-8');
	if data == '':
		continue;
	timestamp = int(line_split[2])/1000;
	date_str = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M');
	url = line_split[3];
	url_type = line_split[4];
	user_num = line_split[7];
	if(url=="" and data=="" and url_type!="image/jpeg"):
		continue;
	if(url_type=="image/jpeg"):
		data_type = url.split("/")[-1].replace(".enc",".jpeg");
	else:
		data_type = "text";
	if(groupid.find("@g.us")==-1):
		continue;
#	groupid = (temp_dict[groupid]).encode('utf-8');
	if(groupid in dict_groups):
		tmp = dict_groups[groupid];
		tmp[timestamp] = data + "\t" + user_num + "\t" + date_str + "\t" + data_type;
		dict_groups[groupid] = tmp;
	else:
		tmp = {};
		tmp[timestamp] = data + "\t" + user_num + "\t" + date_str + "\t" + data_type;
		dict_groups[groupid] = tmp;

tmp_str = '<!DOCTYPE html><html><head><meta charset="UTF-8" name=viewport content="width=device-width, initial-scale=1"><link rel=stylesheet type=text/css href=whatsapp.css><style class=cp-pen-styles>body{background:#ece5dd;font-family:"Helvetica Neue",Helvetica}.container{width:75%;margin:0 auto}.msg{width:100%;height:auto;display:block;overflow:hidden}.msg .bubble{float:left;max-width:75%;width:auto;height:auto;display:block;background:#ebebeb;border-radius:5px;position:relative;margin:10px 0 3px 25px;box-shadow:0 2px 1px rgba(0,0,0,0.2)}.msg .bubble.alt{margin:10px 25px 3px 0;background:#dcf8c6;float:right}.msg .bubble.follow{margin:2px 0 3px 25px}.msg .bubble.altfollow{margin:2px 25px 3px 0;background:#dcf8c6;float:right}.msg .bubble .txt{padding:8px 0 8px 0;width:100%}.msg .bubble .txt .name{font-weight:600;font-size:14px;display:inline-table;padding:0 0 0 15px;margin:0 0 4px 0;color:#3498db}.msg .bubble .txt .name span{font-weight:normal;color:#b3b3b3;overflow:hidden}.msg .bubble .txt .name.alt{color:#2ecc51}.msg .bubble .txt .message{font-size:14px;font-weight:500;padding:0 15px 0 15px;margin:auto;color:#2b2b2b;display:table}.msg .bubble .txt .timestamp{font-size:11px;margin:auto;padding:0 15px 0 0;display:table;float:right;position:relative;text-transform:uppercase;color:#999}.msg .bubble .bubble-arrow{position:absolute;float:left;left:-11px;top:0}.msg .bubble .bubble-arrow.alt{bottom:20px;left:auto;right:4px;float:right}.msg .bubble .bubble-arrow:after{content:"";position:absolute;border-top:15px solid #ebebeb;border-left:15px solid transparent;border-radius:4px 0 0 0;width:0;height:0}.msg .bubble .bubble-arrow.alt:after{border-top:15px solid #dcf8c6;transform:scaleX(-1)}@media only screen and (max-width:450px){.container{width:100%}.timestamp{display:none;color:red}}</style></head><body><div id=mySidebar class=sidebar><a href=javascript:void(0) class=closebtn onclick=closeNav()>X</a>\n';

count = 0;
tmp_str1 = "";
for group in dict_groups.keys():
	out = open(html_location + "/" + group + ".html","w");
	out.write(tmp_str + "\n");
	tmp_str1 += '<a href="' + group.encode('utf-8') + '.html">' + group.encode('utf-8') + '</a>\n';
	count += 1;
#	if(count>5):
#		break;
	out.close();

out_homepage = open(html_location + "/homepage.html","w");
out_homepage.write(tmp_str + "\n");
out_homepage.write(tmp_str1 + "\n");
tmp_str_homepage = '</div><button class=openbtn onclick=openNav()>Toggle Sidebar</button><div class=container><p>Select a group by clicking on the toggle sidebar button</p>\n</div><script>function openNav() {document.getElementById("mySidebar").style.width = "250px";document.getElementById("main").style.marginLeft = "250px";} function closeNav() { document.getElementById("mySidebar").style.width = "0"; document.getElementById("main").style.marginLeft= "0";}</script></body></html>';
out_homepage.write(tmp_str_homepage);
out_homepage.close();

count = 0;
for group in dict_groups.keys():
	out = open(html_location + "/" + group + ".html","a");
	out.write(tmp_str1);
	count += 1;
#	if(count>5):
#		break;
	out.close();

count = 0;
for group in dict_groups.keys():
	out = open(html_location + "/" + group + ".html","a");
	tmp_str = '</div><button class=openbtn onclick=openNav()>Toggle Sidebar</button><div class=container>\n';
	group_data = dict_groups[group];
	sorted_data = sorted(group_data.items(), key=itemgetter(0));
	count_group = 0;
	prev_usernum = '';
	for val in sorted_data:
		timestamp = val[0];
		data_split = val[1].split("\t");
		message_data = data_split[0].replace("'","");
		user_num = data_split[1];
		date_str = data_split[2];
		consec = 1;
		if(count_group%2==0 or (prev_usernum == user_num and consec == 1)):
			tmp_str += '<div class="msg"><div class="bubble"><div class="txt">\n';
			tmp_str += '<span class="name">' + user_num + '</span>\n';
			tmp_str += '<span class="timestamp">' + date_str + '</span>\n';
			tmp_str += '<span class="message">' + message_data + '</span></div><div class="bubble-arrow"></div></div></div>\n';
			consec = 1;
		else:
			tmp_str += '<div class="msg"><div class="bubble alt"><div class="txt">\n';
			tmp_str += '<span class="name">' + user_num + '</span>\n';
			tmp_str += '<span class="timestamp">' + date_str + '</span>\n';
			tmp_str += '<span class="message">' + message_data + '</span></div><div class="bubble-arrow alt"></div></div></div>\n';
			consec = 2;
		count_group += 1;
		prev_usernum = user_num;
	tmp_str += '</div><script>function openNav() {document.getElementById("mySidebar").style.width = "250px";document.getElementById("main").style.marginLeft = "250px";} function closeNav() { document.getElementById("mySidebar").style.width = "0"; document.getElementById("main").style.marginLeft= "0";}</script></body></html>';
	out.write(tmp_str);
	out.close();
	count += 1;
#	if(count>5):
#		break;

#print tmp_str;
