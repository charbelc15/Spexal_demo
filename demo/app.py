#app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql
 
app = Flask(__name__)
app.secret_key = 'Charbel123'

mysql = MySQL()

   
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'testingdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def Index():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
 
    cur.execute('SELECT * FROM employee')   #fetching all info from DB in cursor 
    data = cur.fetchall()
  
    cur.close()
    return render_template('index.html', employee = data) # sending them to index.hml

@app.route('/add_employee', methods=['POST']) #connected to the url form in index.html 
def add_employee():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':            #retrieving variables from from + sending them to DB
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        Address = request.form['Address']
        Department = request.form['Department']
        cur.execute("INSERT INTO employee (name, email, phone, Address, Department) VALUES (%s,%s,%s,%s,%s)", (fullname, email, phone,Address,Department))
        conn.commit()
        flash('Employee Added successfully')
        return redirect(url_for('Index'))
 
#starting the app 
if __name__ == "__main__":
    app.run(port=3000, debug=True)
