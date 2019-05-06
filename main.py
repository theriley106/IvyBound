import requests
import bs4

URL = "https://talk.collegeconfidential.com/columbia-school-general-studies/2126809-columbia-gs-fall-2019-early-regular-decision-thread-p22.html"

def grabSite(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	return requests.get(url, headers=headers)

def get_page_count(url):
	res = grabSite(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	return int(page.select(".LastPage")[0].getText())

class Search(object):
	"""docstring for Search"""
	def __init__(self, urlVal):
		self.main_url = urlVal
		self.thread = urlVal.partition(".com/")[2].partition("/")[0]
		print("Searching for {}".format(self.thread))
		self.pages = get_page_count(self.main_url)
		print("{} Pages found in the {} thread".format(self.pages, self.thread))
		

if __name__ == '__main__':
	#thread = raw_input("College Confidential Thread URL: ")
	thread = "https://talk.collegeconfidential.com/columbia-school-general-studies/"
	# IE: https://talk.collegeconfidential.com/columbia-school-general-studies/
	
	cc = Search(thread)
