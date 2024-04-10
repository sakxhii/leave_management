from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'leave_management'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3308
app.config['MYSQL_USER'] = 'root'  # Your MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Your MySQL password
app.config['MYSQL_DB'] = 'leave_management'  # Your MySQL database name
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

try:
    mysql.connection.ping(reconnect=True)
    print("MySQL connection established successfully.")
except Exception as e:
    print("Error connecting to MySQL:", e)

@app.route('/')
def index():
    return render_template('index.html')
    # if 'username' in session:
    #     return redirect(url_for('dashboard'))
    # return render_template('login.html')

@app.route('/landing')
def landing():
    return render_template('login.html')

@app.route('/render_signup')
def render_signup():
    return render_template('signup.html')
    
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if username == 'admin' and password == 'admin123':
        session['username'] = username
        return render_template("admin.html")

    if user and user['password'] == password:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', message='Invalid username or password')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM leaves")
        data = cur.fetchall()
        cur.execute("SELECT COUNT(*) as total FROM leaves")
        record_count = cur.fetchone()
        print("Record Count:", record_count)
        return render_template('dashboard.html', username=session['username'], data=data, record_count=record_count)
    else:
        return redirect(url_for('index'))
    
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    mysql.connection.commit()
    cur.close()

    session['username'] = username

    return render_template('login.html', username=session['username'])

@app.route('/apply_leave')
def apply_leave():
    if 'username' in session:
        return render_template('apply_leave.html', username=session['username'])
    else:
        return redirect(url_for('index'))
    
@app.route('/leave_status')
def leave_status():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM leaves")
        data = cur.fetchall()
        return render_template('leave_status.html', username=session['username'], data=data)
    else:
        return redirect(url_for('index'))
    
@app.route('/add_leave', methods=['POST'])
def add_leave():
    if 'username' in session:
        from_date = request.form['from_date']
        to_date = request.form['to_date']
        select_type = request.form['select_type']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO leaves (from_date, to_date, leave_type) VALUES (%s, %s, %s)", (from_date, to_date, select_type))
        mysql.connection.commit()
        cur.close()

        # session['username'] = username

        return render_template('leave_status.html')

@app.route('/prof_update')
def prof_update():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    # cur.close()
    return render_template('prof_update.html', username=session['username'], data=data)


# ADMIN
@app.route('/manage_employee')
def manage_employee():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        # manage_employee
        data = cur.fetchall()
        return render_template('manage_employee.html', username=session['username'], data=data)
    else:
        return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    # Delete record from database
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE emp_id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
