import urllib2, urllib, cStringIO
import json
from datetime import datetime, timedelta
import time, threading
import sys, os
from random import randint

#indiegogo comment API endpoint. Pick one.
commentsURL = 'https://www.indiegogo.com/private_api/campaigns/triton-world-s-first-artificial-gills-re-breather/comments'
#commentsURL = 'https://www.indiegogo.com/private_api/campaigns/the-skarp-laser-razor-21st-century-shaving/comments/'

#user agent to send in request. Please replace with your own
legitAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
saveFileName = 'comments.json'

#screenshot rendering
screenshotRenderingActive = False
if screenshotRenderingActive:
	from PIL import Image, ImageFont, ImageDraw 
	font = ImageFont.truetype("Roboto-Regular.ttf", 50)
	fontBold = ImageFont.truetype("Roboto-Bold.ttf", 50)
	cutout = Image.open("cutout.png")
	stamp = Image.open("stamp.png")

#twitter
twitterActive = False
if twitterActive:
	import tweepy
	CONSUMER_KEY = 'blablablablabla'
	CONSUMER_SECRET = 'foobarfoobarfoobarfoopubfoobar'
	ACCESS_KEY = 'beepboopbeepboopbeepboop'
	ACCESS_SECRET = 'pewpewpewpewkillallhumanspewpewpew'
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	twitter = tweepy.API(auth)

def selfCheck():
	for directory in ['renders', 'backups', 'dumpedComments']:
		if not os.path.exists(directory):
			os.makedirs(directory)

def readFile(fileName):
	global tc
	try:
		with open(fileName, 'r') as infile:
			tc = json.load(infile)
	except:
		#no file?
		tc = []

def saveFile(fileName):
	global tc
	with open(fileName, 'w') as outfile:
		json.dump(tc, outfile)

def log(message):
	timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	message = str(message)
	print timestamp + " " + message

def getCommentFromList(id, cList):
	for p in cList:
		if p['id'] == int(id):
			return p
	return False

def fetchComments():
	try:
		headers = { 'User-Agent' : legitAgent }
		req = urllib2.Request(commentsURL, None, headers)
		response = urllib2.urlopen(req)
		data = json.load(response)   

		comments = data['response']
		return comments
	except:
		print "error while fetching comments!"
		return False

def renderScreenshot(comment):
	#rendering the comment image in 2x supersampling, that is 2024x1012, to get an end result of 1024x512
	img = Image.new("RGBA", (2024,1012), (255,255,255))
	draw = ImageDraw.Draw(img)
	draw.fontMode = 1
	draw.text((250, 120), comment['account_name'],(0,0,0),font=fontBold)

	#write the rest of the comment
	text = comment['comment'].split()
	line = ""
	ypos = 180;
	for word in text:
		temp = line + word + " "
		if font.getsize(temp)[0] > 1700:
			#too long, print and carry!
			draw.text((250, ypos), line, (11,11,11), font=font)
			ypos += 64
			line = word + " "
		else:
			line = temp
	draw.text((250, ypos), line, (11,11,11), font=font)

	thumbFile = cStringIO.StringIO(urllib.urlopen(comment['avatar_url']).read())
	thumb = Image.open(thumbFile)
	thumb = thumb.resize((160,160), Image.ANTIALIAS)
	thumb = thumb.convert("RGBA")
	thumb.paste(cutout, (0,0), cutout)
	img.paste(thumb, (40, 126))
	
	img.paste(stamp, (1200, ypos), stamp)

	out = img.resize((1012,506), Image.ANTIALIAS)
	
	renderFileName = 'renders/' + str(comment['id'])+'.png'
	out.save(renderFileName)
	return renderFileName

#used when we DO NOT render screenshots, and instead want text files with the deleted comments
def saveCommentToTextFile(comment):
	filePath = 'dumpedComments/' + str(comment['id']) + '.txt'
	with open (filePath, 'w') as outfile:
		outfile.write(comment['account_name'])
		outfile.write('\n')
		outfile.write(comment['comment'])
		outfile.write('\n')
		outfile.write('---- DELETED ----')

def processNew(comment):
	global tc
	comment['deleted'] = False
	comment['date_added'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
	tc.append(comment)
	log(" new comment found!")
	saveFile(saveFileName)	

def processNewlyDeleted(comment):
	global tc
	comment['deleted'] = True
	comment['date_deleted'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
	log("found newly deleted comment!!!\n")
	print comment['comment'].encode('utf-8', 'ignore')
	saveFile(saveFileName)
	if screenshotRenderingActive:
		screenshot = renderScreenshot(comment)
	else:
		saveCommentToTextFile(comment)
	if twitterActive:
		twitter.update_with_media(screenshot, "Just deleted this")

def sniff():
	log("Fetching!")
	global tc
	official = fetchComments()
	if official != False:
		official.reverse()
		#check for new comments by comparing current official list with our stored "tc" list
		for comment in official:
			if getCommentFromList(comment['id'], tc) == False:
				processNew(comment)
		
		#check for deleted comments, that is check if our last 9 stored comments are in the "oficial" list
		for comment in tc[-9:]:
			if comment['deleted'] == True:
				continue #ignore comments already marked as deleted
			if getCommentFromList(comment['id'], official) == False:
				processNewlyDeleted(comment)
	#plan next sniff in 60 to 120 seconds. DON'T PUSH THIS TOO FAR! HAVE RESPECT FOR THE INDIEGOGO SERVERS. DO NOT DO ANYTHING THAT A HUMAN WOULD NOT DO
	if not sys.flags.interactive:
		sys.stdout.flush() #comes in handy when saving output to nohup.out
		threading.Timer(randint(60, 120), sniff).start()

def autoSave():
	fileName = 'backups/tc-backup-'
	fileName += str(datetime.now().month) + '-'
	fileName += str(datetime.now().day) + '-'
	fileName += str(datetime.now().hour) + '-'
	fileName += str(datetime.now().minute)
	fileName += '.json'
	saveFile(fileName)
	#plan next backup save in 12h
	if not sys.flags.interactive:
		threading.Timer(43200, autoSave).start()

selfCheck()
readFile(saveFileName)
#if the script was started with the '-i' flag for interactive, we dont want it to sniff automaticaly
#this is a good way to debug the script or analyze information in the saved comments
if sys.flags.interactive:
	print "Interactive mode ready"
else:
	print "Autonomous mode running"
	sniff()
	autoSave()