    # script to go through a list of whatsapp groups and join them.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys,time,random
from selenium.webdriver.remote.remote_connection import LOGGER
import logging,os
LOGGER.setLevel(logging.WARNING)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# encoding=utf8 
reload(sys)  
sys.setdefaultencoding('utf8')
 
#f = open("already_joined_groups.txt");
#lines = f.readlines();
dict_already_joined = {};

#for line in lines:
#    line = line.strip();
#    dict_already_joined[line] = 1;
#unaj = open("unable_join_groups.txt");
#lines = unaj.readlines();
dict_unable_join = {};
#for line in lines:
#	line = line.strip("\n");
#	dict_unable_join[line] = 1;

# Replace below path with the absolute path
# to chromedriver in your computer

#chrome_options = Options()
#chrome_options.add_argument('--dns-prefetch-disable')
driver = webdriver.Chrome()
#driver = webdriver.Chrome();
#driver = webdriver.Firefox(executable_path='/Users/kgarimella/Downloads/geckodriver');
driver.set_page_load_timeout(100) 
 
filename = sys.argv[1];
f = open(filename); # file containing the links to the whatsapp groups
lines = f.readlines();
count = 0;
un_count=0;
already_count =0;
net_count =0;
driver.get("https://web.whatsapp.com");
wait = WebDriverWait(driver, 300)

time.sleep(10); # sleep for some time while I use my phone to scan the QR code


for line in lines:
    line = line.strip("\n");
    try:
#    for i in range(1,2):
        group_id = line.split("/")[-1];
#        title = line_split[1];
#        if(title == ""):
#            continue;
        if(group_id in dict_already_joined):
		print >> sys.stderr, "already joined", group_id;
		already_count += 1;
		st2 = open("dup_groups.txt", "a");
		st2.write(group_id + "\n");
		st2.close();
		continue;
        url = "https://web.whatsapp.com/accept?code=" + group_id;
        print >> sys.stderr, "processing", url;
        driver.get(url);
##        sleep_time = random.randint(5,10);
##        time.sleep(sleep_time); # allow time for page to load
#    for i in range(1,2):
##        driver.execute_script("window.focus();");
#        join_button = driver.find_element_by_css_selector("#action-button");
#        print >> sys.stderr, "clicked join button", group_id;
#        join_button.click();
#        if(count==1):
#            time.sleep(50); # sleep first time for some time to allow for scanning the qr code
#            count += 1;
#        else:
#            sleep_time = random.randint(9,10);
#            print >> sys.stderr, "sleeping for", sleep_time;
#            time.sleep(sleep_time); # allow time for page to load
        sleep_time = random.randint(20,30);
        print >> sys.stderr, "sleeping for", sleep_time;
        time.sleep(sleep_time); # allow time for page to load
#        group_info = WebDriverWait(driver, sleep_time).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Join group')]")));
        buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Join group')]")
        if(len(buttons)>0):
            print >> sys.stderr, "button found"
	else:
	    if(group_id in dict_unable_join):
	     	print("already written");
            else:
	    	print >> sys.stderr, "unable to join (revoked)", line;
	    	new=open("unable_join_groups.txt", "a");
	    	new.write(group_id + "\n");
	    	new.close();
		un_count += 1;
        for btn in buttons:
            print "clicked";
            btn.click()
            out = open("already_joined_groups.txt","a");
            out.write(group_id + "\n");
            out.close();
	    count += 1;
#        group_info = driver.find_element_by_css_selector(".popup-body");
#        out = open(directory + "/" + group_id,"w");
#        print >> sys.stderr, "saving info";
#        out.write(group_info.get_attribute('innerHTML') + "\n");
#        out.close();
#        join_group_button = WebDriverWait(driver, sleep_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-plain.btn-default.popup-controls-item")));
#        join_group_button = driver.find_element_by_css_selector(".btn-plain.btn-default.popup-controls-item");
#        print >> sys.stderr, "joined group", group_id;
        sleep_time = random.randint(0,2);
        time.sleep(sleep_time); # allow time for page to load
        print >> sys.stderr, "sleeping for", sleep_time;
#        if(not 
#        try:join_group_button.find_element_by_xpath("//*[contains(text(), 'Retry Now')]")):
#        join_group_button.click();
    except:
	namenet = open("net_unable_join_groups.txt", "a");
	namenet.write(group_id + "\n");
	namenet.close();
	net_count += 1;
        print >> sys.stderr, "unable to join group", line;
#        pass;

driver.close();
print 'Already Joined Found',  already_count;
print 'Just Now Joined',  count;
print 'Unable to Join',  un_count;
print 'Unable to Join Due to netwrok error', net_count;
