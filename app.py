import flask
from flask import Flask, render_template
from somewhere import somewhere

app = flask.Flask(__name__)
##app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def index():

	stringa,stringb,minutes,location = somewhere()

	return render_template("index.html", stringa=stringa, stringb=stringb, minutes=minutes, location=location)
