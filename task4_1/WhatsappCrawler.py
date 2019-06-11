import time
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message, MediaMessage, MMSMessage
import sys
from PIL import Image
from webwhatsapi.helper import safe_str
from webwhatsapi.objects.contact import Contact
from django.utils.encoding import smart_str, smart_unicode

import os




all_files = dict()
all_files['image'] = dict()
all_files['video'] = dict()
all_files['audio'] = dict()

def get_messages_by_group(driver):

    msg_list = driver.get_unread(include_me=False, include_notifications=False, use_unread_count=False)
    return msg_list


def get_image_from_message(message):
    path = './'
    if message.type == 'image':
            try:
                all_files['image'] [message.filename] += 1
                
            except KeyError as e:
                all_files['image'] [message.filename] = 1
            
            imageName = 'image'+all_files['image'] [message.filename]+'_'+message.filename
            message.filename = imageName
            print('-- Image Media')
            print('filename', message.filename)
            print('size', message.size)
            print('mime', message.mime)
            msg_caption=''
            chat_id = smart_str(message.chat_id['_serialized']) 
            if hasattr(message, 'caption'):
                msg_caption = smart_str(message.caption)
                print('caption', smart_str(message.caption))
            print('client_url', message.client_url)
            f=open(path+"chat_" +  chat_id+ ".chat.log","a+")
            f.write("[ {sender} | {timestamp} ] sent media chat_{id}\{filename} with caption '{caption}'\n".format(sender=message.sender.get_safe_name(), timestamp=message.timestamp, id=chat_id, filename=imageName, caption=msg_caption))
            f.close()
            f=open(path+"safechat_" + chat_id + ".chat.log","a+")
            f.write("[ {sender} | {timestamp} ] sent media chat_{id}\{filename} with caption '{caption}'\n".format(sender=message.sender.get_safe_name(), timestamp=message.timestamp, id=chat_id, filename=imageName, caption=msg_caption))
            f.close()
            if not os.path.exists(path+'chat_{id}'.format(  id = chat_id )):
                        os.makedirs(path+'chat_{id}'.format(   id= chat_id ))
            message.save_media(path)


def get_video_from_message(message):
    path = './'
    if message.type == 'video':
            try:
                all_files['video'] [message.filename] += 1
                
            except KeyError as e:
                all_files['video'] [message.filename] = 1
            
            videoName = 'video'+all_files['image'] [message.filename]+'_'+message.filename
            message.filename = videoName
            print('-- Video Media')
            print('filename', videoName)
            print('size', message.size)
            print('mime', message.mime)
            msg_caption=''
            chat_id = smart_str(message.chat_id['_serialized']) 
            if hasattr(message, 'caption'):
                msg_caption = smart_str(message.caption)
                print('caption', smart_str(message.caption))
            print('client_url', message.client_url)
            f=open(path+"chat_" +  chat_id+ ".chat.log","a+")
            f.write("[ {sender} | {timestamp} ] sent media chat_{id}\{filename} with caption '{caption}'\n".format(sender=message.sender.get_safe_name(), timestamp=message.timestamp, id=chat_id, filename=videoName, caption=msg_caption))
            f.close()
            f=open(path+"safechat_" + chat_id + ".chat.log","a+")
            f.write("[ {sender} | {timestamp} ] sent media chat_{id}\{filename} with caption '{caption}'\n".format(sender=message.sender.get_safe_name(), timestamp=message.timestamp, id=chat_id, filename=videoName, caption=msg_caption))
            f.close()
            if not os.path.exists(path+'chat_{id}'.format(  id = chat_id )):
                        os.makedirs(path+'chat_{id}'.format(   id= chat_id ))
            message.save_media(path)



def get_audio_from_message(message):
    path = './'
    if message.type == 'audio':
            try:
                all_files['audio'] [message.filename] += 1
                
            except KeyError as e:
                all_files['audio'] [message.filename] = 1
            
            audioName = 'audio'+all_files['image'] [message.filename]+'_'+message.filename
            message.filename = videoName
            print('-- Audio Media')
            print('filename', message.filename)
            print('size', message.size)
            print('mime', message.mime)
            msg_caption=''
            chat_id = smart_str(message.chat_id['_serialized']) 
            if hasattr(message, 'caption'):
                msg_caption = smart_str(message.caption)
                print('caption', smart_str(message.caption))
            print('client_url', message.client_url)
            f=open(path+"chat_" +  chat_id+ ".chat.log","a+")
            f.write("[ {sender} | {timestamp} ] sent media chat_{id}\{filename} with caption '{caption}'\n".format(sender=message.sender.get_safe_name(), timestamp=message.timestamp, id=chat_id, filename=message.filename, caption=msg_caption))
            f.close()
            f=open(path+"safechat_" + chat_id + ".chat.log","a+")
            f.write("[ {sender} | {timestamp} ] sent media chat_{id}\{filename} with caption '{caption}'\n".format(sender=message.sender.get_safe_name(), timestamp=message.timestamp, id=chat_id, filename=message.filename, caption=msg_caption))
            f.close()
            if not os.path.exists(path+'chat_{id}'.format(  id = chat_id )):
                        os.makedirs(path+'chat_{id}'.format(   id= chat_id ))
            message.save_media(path)



def get_date_from_message(message):
    t = str(message)
    index = t.find(' at ') + 4
    index2 = index + 10
    date = t[index:index2]
    return date



def get_text_from_message(message, file_t):
 
        if hasattr(message, 'safe_content') and  not isinstance(message, MediaMessage)  and not isinstance(message, MMSMessage):
                print >> file_t, message
                print >> file_t, smart_str(message.content)
                print >> file_t, smart_str(message.sender.id)
        else:
                print >> file_t, smart_str(message) , message.filename
                print >> file_t, smart_str(message.sender.id)
                            





def webCrawler():
    #os.system('export PATH=$PATH:/path/t-/geckodriver')
    
    driver_executable_path="./geckodriver"
    driver = WhatsAPIDriver( driver_executable_path="./geckodriver")

    #driver.firstrun()
    print("Waiting for QR")
    driver.wait_for_login()

    print("Bot started")


    files = {}
    caminho = "./"
    path = './'
    
    today_date = ""    
    file_name = ""
    while True:
        time.sleep(3)
        file_name = "AllMessages_" + today_date[-2:] + ".txt" 
        file_t = open(caminho + file_name, 'a', 0)
        time.sleep(3)
        #try:
        msg_list = driver.get_unread(include_me=False, include_notifications=False, use_unread_count=False)
        if len(msg_list) == 0: continue
        
        for i in msg_list:
            if len(i.messages)>0:
                print >> file_t, i.chat
                for j in i.messages:
                    date = get_date_from_message(j)
                    if today_date != date:  #update day
                            today_date = date
                            file_t.close()
                            file_name = "AllMessages_" + today_date[-2:] + ".txt" 
                            file_t = open(caminho + file_name, 'a', 0)
                  
                    get_text_from_message(j, file_t)
                    get_image_from_message(j)
                    get_video_from_message(j)
                    get_audio_from_message(j)


        #except Exception, err:
         #   sys.stderr.write('ERROR: %sn' % str(err))
          #  if 'Message: Tried to run command without establishing a connection' in str(err):
           #     webCrawler()
                 
    file_t.close()

if __name__ == '__main__':
    webCrawler()