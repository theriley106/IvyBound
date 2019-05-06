import requests
import bs4
KEYWORDS = ["fall", "spring", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
URL = "https://talk.collegeconfidential.com/columbia-school-general-studies/2126809-columbia-gs-fall-2019-early-regular-decision-thread-p22.html"

def grabSite(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	return requests.get(url, headers=headers)

def get_page_count(url):
	res = grabSite(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	return int(page.select(".LastPage")[0].getText())

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

#.CountComments .Number

class Search(object):
	"""docstring for Search"""
	def __init__(self, urlVal):
		self.main_url = urlVal
		self.thread = urlVal.partition(".com/")[2].partition("/")[0]
		print("Searching for {}".format(self.thread))
		self.pages = get_page_count(self.main_url)
		
		self.all_threads = []
		for i in range(1, self.pages+1):
			for v in get_yearly_threads(self.main_url + "//p{}".format(i)):
				self.all_threads.append(v)
		print("{} Pages found in the {} thread".format(self.pages, self.thread))
		print("Valid Threads to search: {}".format(len(self.all_threads)))

if __name__ == '__main__':
	#thread = raw_input("College Confidential Thread URL: ")
	thread = "https://talk.collegeconfidential.com/columbia-school-general-studies/"
	# IE: https://talk.collegeconfidential.com/columbia-school-general-studies/
	
	cc = Search(thread)
