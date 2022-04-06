from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user

@app.route('/')
def survey():
    
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    # print(request.form)
    # return redirect('/')
    if not user.User.validate_user_registration(request.form):
        return redirect ('/')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash,
            'terms_of_service': request.form['terms_of_service']
        }
        print(data['terms_of_service'])
        user_id = user.User.save_user(data)
        session['user_id'] = user_id
        session['first_name'] = request.form['first_name']
        return redirect('/dashboard')

@app.route('/login', methods =['POST'])
def login():
    data = {
        "email": request.form["email"]
    }
    user_in_db = user.User.get_user_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    if 'user_id'in session:
        return render_template('dashboard.html')
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')