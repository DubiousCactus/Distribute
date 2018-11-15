import os
import json
import errno

from node import Node
from subprocess import call
from werkzeug import secure_filename
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class REST:

    def __init__(self, controller, ip, port):
        self.controller = controller
        self.ip = ip
        self.port = port

    @app.route('/')
    def showpage():
        return render_template('upload.html')

    @app.route('/storage', methods = ['GET','POST'])
    def upload_file():
        if request.method == 'POST':
            self.controller.store(
                secure_filename(request.files['file'].filename)
            )
            response = jsonify({"msg": 'File uploaded successfully.'})
            response.status_code = 200
            return response
        elif request.method == 'GET':
            response = jsonify({'msg': 'Not implemented'})
            response.status_code = 404
            return response

    def start(self):
        app.run(debug=True, host=self.ip, port=self.port)
