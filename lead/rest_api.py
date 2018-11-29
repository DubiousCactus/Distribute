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
    def show_page():
        return render_template('upload.html')


    @app.route('/storage', methods=['POST'])
    def upload_file():
        self.controller.store(
            secure_filename(request.files['file'].filename)
        )
        response = jsonify({"msg": 'File uploaded successfully.'})
        response.status_code = 200
        return response


    @app.route('/storage/{file_name}', methods=['GET'])
    def download_file():
        file = self.controller.retrieve(
            secure_filename(request.filen_name)
        )
        response = jsonify({"content": file})
        response.status_code = 200
        return response


    @app.route('/strategy/{choice}', methods=['POST'])
    def set_strategy():
        self.controller.set_strategy(request.choice)


    def start(self):
        app.run(debug=True, host=self.ip, port=self.port)
