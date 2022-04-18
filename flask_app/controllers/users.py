from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user, pool

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
        user_id = user.User.save_user(data)
        session['user_id'] = user_id
        session['first_name'] = request.form['first_name']
        return redirect('/dashboard')
        
@app.route('/add-staff-page')
def add_staff_page():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            "user_id": session['user_id']
        }    
        return render_template('add_staff.html', this_user = user.User.user_with_all_pools(data), all_staff = user.User.get_all_staff())

@app.route('/add-staff-db', methods=['POST'])
def add_staff_db():
    if not user.User.validate_staff_registration(request.form):
        return redirect ('/add-staff-page')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash,
            'admin': request.form['admin'],
        }
        user.User.save_staff_user(data)
        return redirect('/dashboard')

@app.route('/add-staff-pool', methods=['POST'])
def add_staff_member_to_pool():
    data = {
        'staff_id': request.form['staff_id'],
        'pool_id': request.form['pool_id']
    }
    user.User.add_staff_pool(data)
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
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            "user_id": session['user_id']
        }    
        return render_template('dashboard.html', this_user = user.User.user_with_all_pools(data), this_staff = user.User.get_one_staff_with_pools(data))

@app.route('/my_account')
def my_account():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            "user_id": session['user_id']
        }    
        return render_template('my_account.html', this_user = user.User.user_with_all_pools(data))

@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    if not user.User.validate_edit_profile(request.form):
        return redirect ('/my_account')
    else:
        data = {
            'user_id': session['user_id'],
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
        }
        user.User.edit_profile(data)
        return redirect('/my_account')

@app.route('/change_password', methods=['POST'])
def change_password():
    if not user.User.validate_change_password(request.form):
        return redirect ('/my_account')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'user_id': session['user_id'],
            'password': pw_hash,
        }
        user.User.change_password(data)
        return redirect('my_account')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')