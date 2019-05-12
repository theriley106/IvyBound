from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import main

app = Flask(__name__, static_url_path='/static')


@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/handle_data', methods=['POST'])
def handle_data():
    thread = request.form['projectFilepath']
    return jsonify(main.search_all(thread))
    # your code
    # return a response

@app.route('/test', methods=['GET'])
def testPage():
	return render_template("index1.html")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)
