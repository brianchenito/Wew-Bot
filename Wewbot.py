import sys
import praw
import time
import loginCredentials as cred # this only exists locally, you need to make your own
import approvedSubs

class WewBot():
	def __init__(self):
		global r # because there can only be one instance of this alive 
		r=praw.Reddit(user_agent="WewBot0.1 by /u/brianchenito ")
		r.set_oauth_app_info(cred.redditId,cred.redditSecret,cred.redirectUri)
		self.refreshToken()
		self.authenticatedUser=r.get_me()

	def refreshToken(self): 
		r.refresh_access_information(cred.redditRefresh)


	def checkComments(self,subReddit): #searches front page for keywords via recurseComments(), launching point for other funcs
		currentSub=r.get_subreddit(subReddit)
		currentComments=currentSub.get_comments(limit=5000)
		self.recurseComments(currentComments)

	def recurseComments(self,comments):
		for comment in comments:
			print(".", end="")
			if "wew" in str(comment.body).lower() or "ｗｅｗ" in str(comment.body).lower() or "w e w" in str(comment.body).lower() :
				print("\nComment: {0} ".format(comment.body))
				if self.wewCheck(comment):
						print("\n okay to comment, commenting:\nＷＥＷ ＬＡＤ\n\nＥ\n\nＷ\n\n \n\nＬ\n\nＡ\n\nＤ")
						comment.reply("ＷＥＷ ＬＡＤ\n\nＥ\n\nＷ\n\n \n\nＬ\n\nＡ\n\nＤ")
						time.sleep(500)

	def wewCheck(self,comment): #checks if a comment containing "wew lad is already present"
		commentsCheck= comment.replies
		try:
			for comment in commentsCheck:
				if  "lad" in str(comment.body).lower() or "ｌａｄ" in str(comment.body).lower() or "l a d" in str(comment.body).lower():
					print("found wew lad already in comments")
					return False	
			print("no reply 'wew lad' found")
			return True
		except AttributeError:
			print(" hit moreComments(), safe to assume an 'wew lad' is not present")
			return True

if __name__ == "__main__":
		bot=WewBot()

		while True:
			print("Active Bot: {0}".format(bot.authenticatedUser))
			bot.checkComments(approvedSubs.approved)
			bot.refreshToken()
			print("refreshing search\n")
