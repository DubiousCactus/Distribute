import os
import json
import errno

from node import Node
from subprocess import call
from flask import Flask, render_template, request

app = Flask(__name__)

class RestApi:

    def __init__(self, nodes, ip, port):
        self.ip = ip
        self.port = port

    @app.route('/')
    def showpage():
       return render_template('upload.html')

    @app.route('/storage', methods = ['GET','POST'])
    def upload_file():
       if request.method == 'POST':
          f = request.files['file']
          f.save(secure_filename(f.filename))
          # (TESTING REPLICAITON)
          # IF TRUE SEND TO RANDOM NODE 
          # ELSE SEND TO X NODES
          return { "code": 200, "msg": 'File uploaded successfully.' }

       if request.method == 'GET':
           # GET THE FILE FROM A NODE
             return 'returned '+ request.args["filename"]+' successfully'
             #return 'returning '+ fileEntered +' successfully'

    def start(self):
        app.run(debug=True, host=self.ip, port=self.port)
        
