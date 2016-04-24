import datetime
import urllib2
import json
import time
import smtplib,email

from Logger import Logger
from decimal import *

# Config
# 60 sec update rate
sleepTime = 60 
# coin name
coin = 'TEK'
difficultyTrigger = 0.00008 
# mail
host = 'smtp.mail.yahoo.com'
#host = 'smtp.live.com'
port = 587

username = "yuenbenny68@yahoo.com"
password = "#'a]&S[/v3N4gv6{KO"
fromaddr = "yuenbenny68@yahoo.com"
toaddrs  = "betgurujackg@gmail.com"

timeBetweenEmails = 3600 # 1 hour in sec


# Code

aboveTrigger = False

log = Logger()

def timestamp():
	ts = time.time()
	return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def sendEmail():

	msg = email.message_from_string('do something!')
	msg['From'] = fromaddr
	msg['To'] = toaddrs
	msg['Subject'] = coin + 'difficulty below ' + str(difficultyTrigger)


	# The actual mail send	
	server = smtplib.SMTP(host, port)
	server.set_debuglevel(1)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(username, password)
	server.sendmail(fromaddr, toaddrs, msg.as_string())
	server.quit()  
	log.log('Mail Sent')

lastSentTS = 0 #init timestamp
try:
	log.log('Started')
	while True:
		try:
			ret = urllib2.urlopen(urllib2.Request('http://presstab.pw/phpexplorer/'+coin+'/api.php'))
			jsonRet = json.loads(ret.read())
			currentDifficulty = Decimal(jsonRet[0]['difficulty'])
			log.refreshStatus(timestamp() + ' ' + coin +' difficulty:' + str(currentDifficulty))

			if(currentDifficulty <= difficultyTrigger):
				if(time.time() > lastSentTS + hour and aboveTrigger):
					sendEmail()
					lastSentTS = time.time()
					aboveTrigger = False
			else:
				aboveTrigger = True

		except Exception as e:
			log.log("ERROR: " + str(e))
			pass		
		time.sleep(sleepTime)
except KeyboardInterrupt:
	log.log('Bye')
	exit(0)