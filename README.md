# Whatsapp_Tutorial

Code for exploring WhatsApp. Presented during the tutorial titled 'Tools for WhatsApp data collection' presented at ICWSM 2019.
URL: https://users.ics.aalto.fi/kiran/whatsapp-tutorial/

The tutorial slides can be found on the website provided above.

Getting data from WhatsApp can be organized into 4 parts or 'tasks'.

1. Find relevant groups
2. Join them on the phone
3. Backup the database
4. Extract messages (Download messages, images, videos, etc.)

We provide code to perform each of these tasks.

Task 1. Contains code to automatically search google for whatsapp group links. Given a search query, we can find the relevant groups.

Task 2. Code to join the groups automatically (mostly replication of https://github.com/gvrkiran/whatsapp-public-groups)

Task 3. Extracting data from the phone. Has tools to decrypt the database from WhatsApp, if you have the key. If not, there are other ways to extract the date. See the slides for info.

Task 4. Processing the extracted data. Downloading images, converting the databases to CSV files, etc.

Authors: Philipe Melo, Kiran Garimella.
