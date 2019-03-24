#from metadata import mod
from applyfilter import filtering
from retrievefile import case_retrieve
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Hello, World!"


#app.register_blueprint(mod, url_prefix='/metadata')
app.register_blueprint(filtering, url_prefix="/filter")
app.register_blueprint(case_retrieve, url_prefix="/case")
if __name__ == '__main__':
    app.run()
