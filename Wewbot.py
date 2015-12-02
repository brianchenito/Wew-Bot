import sys
import praw
import time
import loginCredentials as cred # this only exists locally, you need to make your own
import approvedSubs
import re


def safeprint(safe): # to help handle weird unicode stuff, its not gonna render right but it wont throw errors
	try:
		print(safe)
	except UnicodeEncodeError:
		if sys.version_info >= (3,):
			print(safe.encode('utf8').decode(sys.stdout.encoding))
		else:
			print(safe.encode('utf8'))

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
			if set(re.findall(r'\b(%s)\b' % '|'.join(["wew","ｗｅｗ","w e w"]), str(comment.body).lower())):
				safeprint("\nComment: {0} ".format(comment.body))
				if len(comment.body.split())<3:
					if self.wewCheck(comment):
						safeprint("\n okay to comment, commenting.")
						comment.reply("Ｗ Ｅ Ｗ  Ｌ Ａ Ｄ\n\nＥ\n\nＷ\n\n \n\nＬ\n\nＡ\n\nＤ")
						time.sleep(300)
				else:
					print(" comment is too long, probably not relevant")	

	def wewCheck(self,comment): #checks if a comment containing "wew lad is already present"

		commentsCheck= comment.replies
		try:
			for comment in commentsCheck:
				if "Ｌ Ａ Ｄ" in str(comment.body):
					print("found wew lad already in comments")
					return False
				if str(comment.author)=="Wew_Bot":
					return False
			print("no reply 'wew lad' found")
			return True
		except AttributeError:
			print(" hit moreComments()")
			return False

if __name__ == "__main__":
		bot=WewBot()

		while True:
			try:# sometimes the api times out, or the servers go down
				print("Active Bot: {0}".format(bot.authenticatedUser))
				bot.checkComments(approvedSubs.approved)
				bot.refreshToken()
				print("\nrefreshing search")
			except Exception as e:
				print("\nError {0}".format(str(e)))
				time.sleep(300)
				pass
			