from flask import Flask

app = Flask(__name__)
app.secret_key = "82jadiaks129eioadw[awdap=;'wd]"

from routes import *