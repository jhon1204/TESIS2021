import flask
from flask import request, jsonify


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for QAira Data.</p>"

@app.route('/qaira', methods=['GET'])
def getQaira():
    message="Success"
    try:
        print('')
    except:
        message="Error al actualizar las mediciones"
    return jsonify()

app.run()