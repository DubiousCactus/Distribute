import os
import json
import errno

from node import Node
from subprocess import call
from werkzeug import secure_filename
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
controller = None
ip = None
port = None


class REST():

    def __init__(self, ctrl, host, p):
        global controller, ip, port
        controller = ctrl
        ip = host
        port = p


    @app.route('/', methods=['GET'])
    def show_page():
        return render_template('upload.html', rest_host=ip, rest_port=port,
                               entries=controller.get_ledger_entries())


    @app.route('/storage', methods=['POST'])
    def upload_file():
        if 'file' in request.files:
            success = controller.store(
                secure_filename(request.files['file'].filename),
                request.files['file']
            )
            if success:
                response = jsonify({"msg": 'File uploaded successfully.'})
                response.status_code = 200
                return response
            else:
                response = jsonify({"msg": "File couldn't be written to nodes."})
                response.status_code = 500
                return response
        return jsonify({"msg": "File not present in request"})


    @app.route('/storage/', methods=['GET'])
    def download_file():
        if 'file_name' in request.args:
            file = controller.retrieve(
                secure_filename(request.args.get('file_name'))
            )
            if file:
                response = jsonify({"content": file})
                response.status_code = 200
                return response
            else:
                response = jsonify({"msg": "File couldn't be found."})
                response.status_code = 500
                return response
        return jsonify({"msg": "File name not present in request"})



    @app.route('/strategy/{choice}', methods=['POST'])
    def set_strategy():
        controller.set_strategy(request.choice)


    def start(self):
        app.run(debug=True, host=ip, port=port)
