from flask import Flask,request,render_template,url_for,redirect,session,flash
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps
import time,os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'erecipies'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql =  MySQL(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT,'static/')

"""*********************Index page and search handler*******************************"""
@app.route('/',methods=['GET','POST'])# Home page
def index():
    cur = mysql.connection.cursor()
    if request.method == "POST":
        food = request.form['food']
        cur.execute("SELECT * FROM recipies WHERE MATCH(title,steps) AGAINST(%s)",[food])
        results = cur.fetchall()
        cur.close()
        return render_template('results.html',results=results)
    else:
        return render_template("index.html")
"""*******************************************************************************************************************"""

"""***************Decorator definition for login_required******************"""        
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap
"""******************************************************"""

"""*********************Add recipie aand user registration handlers*************************"""
@app.route('/add_recipie',methods=['GET','POST']) 
@login_required
def add_recipie():
    if request.method == "POST":
        
        title = request.form['title']
        steps = request.form['steps']

        food_img = request.files['food-img']
        img_name = food_img.filename
        destination = '/'.join([target,img_name])
        food_img.save(destination)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO recipies(title,steps,image,author) VALUES(%s,%s,%s,%s)",(title,steps,img_name,session['email']))
        mysql.connection.commit()
        cur.close()
        flash('Recipie Added!!')
        return redirect(url_for('my_recipies'))
    return render_template('add_recipie.html')

@app.route('/register',methods=['GET','POST'])# User register page
def register():
    if request.method == "POST":
        cur = mysql.connection.cursor()
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = sha256_crypt.encrypt(str(request.form['password']))

        existing_name = cur.execute("SELECT * FROM users WHERE name = %s",[name])
        existing_email = cur.execute("SELECT * FROM users WHERE email = %s",[email])
        existing_username = cur.execute("SELECT * FROM users WHERE username = %s",[username])
        if existing_name > 0:
            flash("This name already regsitered!Please choose another",category='info')
            return render_template('register.html')
        if existing_email > 0:
            flash("This Email is already registered!")
            return render_template('register.html')
        if existing_username > 0:
            flash("This username used is already registered!")
            return render_template('register.html')

        cur.execute("INSERT INTO users(name,email,username,password) VALUES(%s,%s,%s,%s)",(name,email,username,password))
        mysql.connection.commit()
        cur.close()
        flash('Registration Success!!')
        return redirect(url_for('login'))
    return render_template('register.html')
"""*****************************************************************************************************************"""

"""******************************User login handler**************************"""
@app.route('/login',methods=['GET','POST'])# User login page
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_entered = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE email = %s",[email])
        if result > 0:
            data = cur.fetchone()
            db_password = data['password']
            usr_name = data['username']

            if sha256_crypt.verify(password_entered,db_password):
                session['logged_in'] = True
                session['email'] = email
                flash('Log In Success!!')
                return redirect(url_for('index'))
            else:
                flash('Details incorrect')
                return render_template('login.html')
            cur.close()
        else:
            flash('User does not exist!!')
            return redirect(url_for('register'))           
    return render_template('login.html')
"""******************************************************************************"""

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


"""******************Shows user profile********************************"""
@app.route('/profile') #user Profile page
@login_required
def profile():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s",[session['email']])
    profile = cur.fetchone()
    cur.close()
    return render_template('profile.html',profile=profile)
"""*********************************************************************"""


"""*******lists all recipies and individual recipies*********"""
@app.route('/my_recipies')
@login_required
def my_recipies():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM recipies WHERE author = %s",[session['email']])
    recipies = cur.fetchall()
    cur.close()
    return render_template('my_recipies.html',recipies=recipies)

@app.route('/single_recipie/<string:id>/')

def single_recipie(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM recipies WHERE id = %s",[id])
    recipie = cur.fetchone()
    return render_template('single_recipie.html',recipie=recipie)
"""***************************************************************"""


"""***********************This code block handles editing and updating recipies*****************************************"""
@app.route('/edit_recipie/<string:id>',methods=['GET','POST'])
@login_required
def edit_recipie(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT title,ingredients,steps FROM recipies WHERE id = %s",[id])
    e_recipie = cur.fetchone()

    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        steps = request.form['steps']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE recipies SET title=%s, ingredients=%s, steps=%s WHERE id = %s",(title,ingredients,steps,id))
        mysql.connection.commit()
        cur.close()
        flash('Recipie Updated!!')
        return redirect(url_for('my_recipies'))
    return render_template('edit_recipie.html',e_recipie=e_recipie)
"""***********************************************************************************************************************"""

"""*******************This code block handles deleting recipies*****************"""
@app.route('/delete_recipie/<string:id>',methods=['GET','POST'])
@login_required
def delete_recipie(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM recipies WHERE id = %s AND author = %s",(id,session['email']))
    mysql.connection.commit()
    cur.close()
    flash('Recipie Deleted!!')
    return redirect(url_for('my_recipies'))
"""********************************************************************"""


"""*****************This code block handles editing and updating user profile*************************"""
@app.route('/edit_profile/<string:id>',methods=['GET','POST'])
@login_required
def edit_profile(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT name,email,username FROM users WHERE id = %s",[id])
    profileDetails = cur.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']

        profile_pic = request.files['profile_pic']
        img_name = profile_pic.filename
        destination = '/'.join([target,img_name])
        profile_pic.save(destination)


        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET name = %s, email = %s, username = %s profile_pic = %s WHERE id = %s",(name,email,username,img_name,id))
        mysql.connection.commit()
        cur.close()
        flash('Profile Updated succesfully!!')
        return redirect(url_for('profile'))
    return render_template('edit_profile.html',profileDetails=profileDetails)
"""******************************************************************************************"""

"""**********************Handles deleting user profile**********************"""
@app.route('/delete_profile/<string:id>',methods=['GET','POST'])
@login_required
def delete_profile(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s",[id])
    mysql.connection.commit()
    cur.close()
    session.clear()
    flash('Account Deleted!!')
    return redirect(url_for('index'))
    
"""*************************************************************************"""

if __name__ == "__main__":
    app.run(debug=True)
