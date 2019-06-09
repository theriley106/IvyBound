from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import main
import bs4
import datetime
import time

app = Flask(__name__, static_url_path='/static')

def parse_comment_html(val):
	info = {}
	htmlString = val['comment']
	page = bs4.BeautifulSoup(htmlString, 'lxml')
	info['username'] = page.select(".Username")[0].getText()
	info['totalPosts'] = page.select("b")[0].getText()
	info['profilePic'] = str(page.select(".ProfilePhotoMedium")[0]).partition('src="')[2].partition('"')[0]
	info['time'] = str(page.select("time")[0]).partition('title="')[02].partition('"')[0]
	info['dtString'] = str(page.select("time")[0]).partition('datetime="')[2].partition('"')[0].partition('T')[0]
	#info['dtString'] =
	#raw_input(info['dtString'])
	info['content'] = page.select(".userContent")[0]
	justification = ""
	if val['type'] == "direct":
		justification += """{} posted their stats <a href="{}">here</a>""".format(info['username'], val['urls'][0])
	else:
		justification = """{} posted their admission decision <a href="{}">here</a><br>""".format(info['username'], val['urls'][0])
		justification += """{} posted their stats <a href="{}">here</a>""".format(info['username'], val['urls'][1])
	info['justification'] = justification
	info['foundVia'] = val['type']
	info['url'] = val['urls'][0]
	info['title'] = ' '.join([x.title() for x in info['url'][::-1].partition('/')[0][::-1].partition('-')[2].replace(".html", "").split("-")])
	return info

def extract_school_name_from_URL(urlString):
	schoolName = urlString.partition('/')[0]
	return schoolName

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
	if request.headers.get("Referer") != None:
		return redirect('http://talk.collegeconfidential.com/' + path)
	#raw_input(request.headers.get("Referer"))
	typeVal = request.args.get('type', None)
	# This is the type of application # IE: Transfer, all, freshman
	# Defaults to all
	collegeThread = extract_school_name_from_URL(path)
	if len(collegeThread) < 5:
		return collegeThread + " is an invalid school name"
	thread = "https://talk.collegeconfidential.com/" + collegeThread
	database = main.search_all(thread, typeVal)

	for keyName in database.keys():
		for i, val in enumerate(database[keyName]):
			database[keyName][i] = parse_comment_html(val)
	database2 = []
	order = ["accepted", "rejected", "unknown"]
	totalCount = 0
	for k in order:
		info = {}
		info["decision"] = k
		info["results"] = sorted(database[k], key= lambda e: datetime.datetime(*time.strptime(e['dtString'], "%Y-%m-%d")[:6]), reverse=True)
		totalCount += len(info['results'])
		database2.append(info)
	return render_template('results.html', database=database2, choices=[database.keys()], resultCount=totalCount)

@app.route('/handle_data', methods=['POST'])
def handle_data():
	thread = request.form['projectFilepath']
	database = main.search_all(thread)

	for keyName in database.keys():
		for i, val in enumerate(database[keyName]):
			database[keyName][i] = parse_comment_html(val)
	database2 = []
	order = ["accepted", "rejected", "unknown"]
	for k in order:
		info = {}
		info["decision"] = k
		info["results"] = sorted(database[k], key= lambda e: datetime.datetime(*time.strptime(e['dtString'], "%Y-%m-%d")[:6]), reverse=True)
		database2.append(info)



	return render_template('results.html', database=database2, choices=[database.keys()])
	# your code
	# return a response

@app.route('/test', methods=['GET'])
def testPage():
	return render_template("index1.html")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)
