# IndieCensor
A bot that tweets DELETED comments from Indiegogo® campaigns
designed to uncover scammer running shady campaigns.
Brought to you by /u/exclamationMarek
Visit reddit.com/r/shittyKickstarters!


# Pre-requisites:
-Python 2.7
-Python Image Library PIL or Pillow for rendering the comments to a png file
	(easily installable in binary form, ex. apt-get install python-imaging)
-Tweepy for tweeting. Can be omitted if you just want to run locally


# File structure:
/indieCensor.py - main script
/comments.json - local copy of the comments. Will be automatically created if not found
/Roboto-bold.ttf and Roboto-regular.ttf - fonts for rendering the comment in .png
/cutout.png - a template to render the Indiegogo profile picture of the commenter properly
/stamp.png - image of the stamp that is superimposed on the rendered comment (note the transparent background!)
/renders/ - folder to store the rendered comment images
/backups/ - folder to store backups of the comments.json file, one backup every 12h

# Operating principle:
The bot refreshes the comment section of the campaign website, by requesting this address:
https://www.indiegogo.com/private_api/campaigns/triton-world-s-first-artificial-gills-re-breather/comments/ (this example is for the triton campaign). This endpoint returns a json file containing:
int count - number of returned comments
dict pagination - information about number of comments, and division on pages
list response - the interesting payload of comments

the response list contains up to 10 latest comments, each represented as a dictionary with various details. We are interested in the following ones:
int id - unique identification number
string account_name - Name of the commenter
string comment - plaintext, UTF-8 encoded comment text

All comment data is stored in the comments.json file, as a list of comments (ALL comments, so the list is longer than 10 positions!)

Every time the URL is fetched, we compare the IDs of the retrieved comments with our local list of comments. If the new fetched listed, the "official" comments per say, contains an ID that is not present in the local copy, that comment is considered new and stored locally. Following this, we check if the 9 most recent comments STORED LOCALLY are among the 10 "official" comments. If there is an ID present in the local copy but ABSENT from the "official" copy, we know that this comment was deleted.

Note that the bot ignores comment replies. Upon some observation it was noted that Indiegogo users seldom use the "reply to comment" feature to raise questions about the validity of a campaign. The campaign owner, in contrast, often replies to comments with what is often simply "more bullshit" therefore this content is omitted by the bot entirely.

# Usage
It's recommended to have the script running in the background, like so:
nohup python indieCensor.py&

For debuging, it's recommended to use the interactive mode. This will disable periodic sniffing
python -i indieCensor.py

# License and stuff
This is an open source project, under GPL 4.0.

The "Roboto" font is  property of Google inc. and Google inc. is awesome.

"Indiegogo" is a trademark of Indiegogo inc. appearing here under fair use.

"Triton" is utter bullshit and its owners should feel bad about themselves.