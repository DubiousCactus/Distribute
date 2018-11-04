#! /usr/bin/python3

from flask import Flask, render_template, request
from werkzeug import secure_filename

app = Flask(__name__)

@app.route('/')
def showpage():
   return render_template('upload.html')

@app.route('/storage', methods = ['GET','POST'])
def upload_file():

   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename)) #WILL BE REMOVED BECAUSE WE DONT STORE ON THE PI3
	  #REMOTE CALL TO RANDOM NODE IN THE SYSTEM USING RPC
      return 'file uploaded successfully'

   if request.method == 'GET':
         return 'returned '+ request.args["filename"]+' successfully'
         #return 'returning '+ fileEntered +' successfully'

if __name__ == '__main__':
	app.run(debug=True, host="172.24.1.1", port=5000)
	print("Running")
