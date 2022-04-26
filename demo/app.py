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

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_employee(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('SELECT * FROM employee WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', employee = data[0])

 
@app.route('/update/<id>', methods=['POST'])
def update_employee(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['Address']
        department = request.form['Department']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE employee
            SET name = %s,
                email = %s,
                phone = %s,
                Department = %s,
                Address = %s
            WHERE id = %s
        """, (fullname, email, phone, department, address, id))
        flash('Employee Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_employee(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('DELETE FROM employee WHERE id = {0}'.format(id))
    conn.commit()
    flash('Employee Removed Successfully')
    return redirect(url_for('Index'))

 
#starting the app 
if __name__ == "__main__":
    app.run(port=3000, debug=True)
