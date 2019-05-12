from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import main
import bs4

app = Flask(__name__, static_url_path='/static')

def parse_comment_html(val):
	info = {}
	htmlString = val['comment']
	page = bs4.BeautifulSoup(htmlString, 'lxml')
	info['username'] = page.select(".Username")[0].getText()
	info['totalPosts'] = page.select("b")[0].getText()
	info['profilePic'] = str(page.select(".ProfilePhotoMedium")[0]).partition('src="')[2].partition('"')[0]
	info['time'] = str(page.select("time")[0]).partition('title="')[02].partition('"')[0]
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

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
	thread = "https://talk.collegeconfidential.com/" + path
	database = main.search_all(thread)

	for keyName in database.keys():
		for i, val in enumerate(database[keyName]):
			database[keyName][i] = parse_comment_html(val)
	database2 = []
	order = ["accepted", "rejected", "unknown"]
	for k in order:
		info = {}
		info["decision"] = k
		info["results"] = database[k]
		database2.append(info)
	return render_template('results.html', database=database2, choices=[database.keys()])

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
		info["results"] = database[k]
		database2.append(info)



	return render_template('results.html', database=database2, choices=[database.keys()])
	return jsonify()
	# your code
	# return a response

@app.route('/test', methods=['GET'])
def testPage():
	return render_template("index1.html")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)
