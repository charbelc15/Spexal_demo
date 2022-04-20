#app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql
 
app = Flask(__name__)
  
@app.route('/')
def Index():
    return render_template('index.html')

#starting the app 
if __name__ == "__main__":
    app.run(port=3000, debug=True)
