# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests
import bs4
import threading
ALL = []
KEYWORDS = ["fall", "spring", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
URL = "https://talk.collegeconfidential.com/columbia-school-general-studies/2126809-columbia-gs-fall-2019-early-regular-decision-thread-p22.html"

def grabSite(url):
	for i in range(3):
		try:
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
			return requests.get(url, timeout=7, headers=headers)
		except Exception as exp:
			print exp
			pass
	return "<html></html>"

def is_stats(string):
	if 'gpa' in string.lower() and (string.count(":") > 2 or string.count("-") > 2):
		return True
	else:
		return False

def get_page_count(url):
	res = grabSite(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	try:
		return int(page.select(".LastPage")[0].getText())
	except:
		return 2

def get_specific_comment(url):
	# Extracts a specific comment ID from a forum page
	commentID = url.partition("_")[2]
	print commentID
	res = grabSite(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	for val in page.select(".Role_RegisteredUser"):
		if "/post/facebook/comment?id=" + commentID in str(val):
			return val.getText()

def dig_further(stringVal):
	# This means the comment on a users page *may* contain stats
	# Enough of a chance to pull the full comment (Another API call)
	s = stringVal.lower()
	return 'accepted' in s or 'rejected' in s or 'decision' in s or '!' in s

def extract_url_from_item(itemVal):
	# Extracts a comment URL from an item selection
	return str(itemVal).partition('a href="')[2].partition('"')[0]

def get_stats_from_profile(profileName):
	# This function tries to extract stats based on a users profile ID
	# If nothing is found it will return None
	url = "https://talk.collegeconfidential.com/profile/comments/{}".format(profileName)
	comments = []
	res = grabSite(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	for item in page.select(".Item"):
		for val in item.select(".Message"):
			if dig_further(val.getText()):
				urlVal = extract_url_from_item(item)
				get_specific_comment(urlVal)

				if is_stats(val.getText()) == True:
					print(val.getText())

def get_yearly_threads(url):
	threads = []
	res = grabSite(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	for val in page.select("tr"):
		x = str(val.select(".DiscussionName")[0].getText())
		if "12" in x:
			found = False
			for v in KEYWORDS:
				if v in str(x).lower():
					found = True
			if found == True:
				for v in val.find_all('a', href=True):
					if 'talk.collegeconfidential.com' in str(v['href']):
						threads.append(v['href'])
						break
	return threads

def gen_thread_url(url, num):
	# https://talk.collegeconfidential.com/columbia-school-general-studies/2036962-dual-ba-program-trinity-college-dublin-and-columbia-university-fall-2018.html
	return url.partition(".html")[0] + "-p{}.html".format(num)

def extract_from_thread_url(url):
	rCount = 0
	aCount = 0
	tempCount = get_page_count(url)
	#print("SEARCHING: {} - {} pages".format(url, tempCount))
	for i in range(1, tempCount+1):
		res = grabSite(gen_thread_url(url, i))
		page = bs4.BeautifulSoup(res.text, 'lxml')
		for comment in page.select(".userContent"):
			if is_stats(str(comment.getText())):
				if 'accepted' in str(comment.getText()).lower():
					print("_____ACCEPTED______")
				elif 'rejected' in str(comment.getText()).lower() or 'rejection' in str(comment.getText()).lower():
					print("_____REJECTED______")
				else:
					print("_____UNKNOWN______")
				print str(comment.getText())
				print("\n\n\n")
			rCount += str(comment).lower().count("rejected")
			aCount += str(comment).lower().count("accepted")
	x = {"url": url, "rCount": rCount, "aCount": aCount}
	ALL.append(x)
	#print x
	return x


#.CountComments .Number

class Search(object):
	"""docstring for Search"""
	def __init__(self, urlVal):
		self.main_url = urlVal
		self.thread = urlVal.partition(".com/")[2].partition("/")[0]
		print("Searching for {}".format(self.thread))
		self.pages = get_page_count(self.main_url)
		self.pages = 15
		self.all_threads = []
		for i in range(1, self.pages+1):
			for v in get_yearly_threads(self.main_url + "//p{}".format(i)):
				#print v
				# Example: 
				self.all_threads.append(v)
		#print("{} Pages found in the {} thread".format(self.pages, self.thread))
		#print("Valid Threads to search: {}".format(len(self.all_threads)))
		threads = [threading.Thread(target=extract_from_thread_url, args=(ar,)) for ar in self.all_threads]
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join()
		for val in ALL:
			print val
		
if __name__ == '__main__':
	#thread = raw_input("College Confidential Thread URL: ")
	#thread = "https://talk.collegeconfidential.com/university-southern-california/"
	# IE: https://talk.collegeconfidential.com/columbia-school-general-studies/
	
	#cc = Search(thread)
	get_stats_from_profile("radishguy")
