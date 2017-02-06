#!/bin/env/python3

import urllib 
from bs4 import BeautifulSoup

# Personal info goes here
target_schools = ['A University', 'University Of B', 'Seattle', 'Boulder']
field_to_search = 'Chemistry'
path = ''

site = "http://thegradcafe.com/survey/index.php?q=" + field_to_search
request = urllib.request.Request(site)
opener = urllib.request.build_opener()
page = opener.open(request)
soup = BeautifulSoup(page, 'lxml')

school_scrape = soup.find_all('td' , class_ = 'instcol')[1:]
schools = []
for i in school_scrape:
	schools.append(i.get_text())


date_scrape = soup.find_all('td' , class_ = 'datecol')
dates = []
for i in date_scrape:
	dates.append(i.get_text())

# Store schools and dates together as a tuple
big_list = list(zip(schools, dates))

target_results = []

# If one of your target schools is in the results, put it in the text file
for i in big_list:
	for j in target_schools:
		if j in i[0]:
			target_results.append("Result found for {} as {} on {}".format(j, i[0], i[1]))

def output_writer(title):
	with open(path + title + '.txt', 'w') as f:
		for line in target_results:
			f.write(str(line) + "\n")
	f.close()

output_writer('new_results')

# Check for output file, correct if first run
try:
	f = open(path + 'old_results.txt', 'r')
except:
	output_writer('old_results')
	print('This is your first time running the script.\n'
		'Check the website for now, the next time you run it you will get updates.')

updates = []

with open(path + 'new_results.txt', 'r') as n:
	n = n.read()
	# If there is an update that wipes all your schools from the first page,
	# rewrite the file to avoid false flags
	if n == '\n' or n == '\n\n' or n == '':
		output_writer('old_results')
	n_l = n.split('\n')
	n_l_size = len(n_l)
	with open(path + 'old_results.txt', 'r') as o:
		o = o.read()
		o_l = o.split('\n')
		o_l_size = len(o_l)
		# Check for new results even if the same number of lines are present
		if o_l_size == n_l_size:
			for i in range(n_l_size):
				if n_l[i] != o_l[i]:
					updates.append(n_l[i])
			output_writer('old_results')
		# Stuck only checking the same amount of lines as the smaller file
		if o_l_size < n_l_size:
			for i in range(o_l_size):
				if n_l[i] != o_l[i]:
					updates.append(n_l[i])
			updates.append('There may be additional updates.')
			output_writer('old_results')

if updates != []:
	print(updates)
else:
	print('No new updates.')

# # GNOME integration for other Linux nerds
# import subprocess

# gnome_update = []

# for i in updates:
# 	if i == 'There may be additional updates':
# 		gnome_update.append(' + more')
# 	else:
# 		gnome_update.append(i[17:24])

# msg = ", ".join(str(i) for i in gnome_update)

# def send_message(message):
# 	subprocess.Popen(['notify-send', message])
# 	return
# if updates != []:
# 	send_message(msg)

# # Email functionality, you'll have to set it up yourself
# import smtplib

# gmail_user = 'your_username' + '@gmail.com'  
# gmail_password = 'your_password'

# outgoing = gmail_user  
# to = gmail_user 
# subject = 'School Admissions Update'  
# body = str(updates)

# email_text = """\  
# outgoing: {}  
# To: {}  
# Subject: {}

# {}
# """.format(outgoing, ", ".join(to), subject, body)

# try:  
#     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#     server.ehlo()
#     server.login(gmail_user, gmail_password)
#     server.sendmail(outgoing, to, email_text)
#     server.close()

#     print 'Email sent!'
# except:  
#     print 'Something went wrong.'
