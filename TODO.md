#TODO:

-Make image rendering optional, just like tweeting is optional, so a bot can run on a machine without PIL and still collect deleted comment data in json format
-Add multiplayer (ability to track many different campaigns at once)
-Randomise the text when posting, for flair and fun!
-Add a censor loop. I know, "irony" and all, but I would rather not tweet something that actualy IS spam, or excessive vulgarity, and the latter is quite common on scam-campaigns. The censor loop may be implemented as follows:
	-bot sends a direct message with the new post to an admin/moderator
	-admin/moderator replies with Y or N
	-bot reads the reply and posts publicly or not, depending on the Y/N answer.
-Make the bot tweet mention a randomly chosen founder of Indiegogo? I mean it's rude to keep them out of the loop, I'm SURE they would react to a scam-campaign misbehaving, even if they earn thousands of dollars on these scams. Right? 
