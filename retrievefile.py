from acts_detector_2 import *
from cases_detector import *
from flask import Blueprint, jsonify, abort, request

case_retrieve = Blueprint('foo2', __name__)
#filename = "1967_M_37.txt"


@case_retrieve.route('/getfileData', methods=['POST'])
def get_data():
    data = request.get_json(force=True)
    filename = data['url']
    #print(getActs1("All_FT/"  + filename))
    f = open("All_FT/" + filename)
    text = f.read()
    a = {}
    a['text'] = text
    a['cases_sited'] = getCases("All_FT/" + filename)
    return jsonify({'data': a})
    #print(getCases("All_FT/" + filename))


@case_retrieve.route('/getActData', methods=['POST'])
def read_data():
    data = request.get_json(force=True)
    filename = data['url']
    f = open(filename)
    text = f.read()
    a = {}
    a['text'] = text
    return jsonify({'data': a})
