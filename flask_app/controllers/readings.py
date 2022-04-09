from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models import user, pool, reading

@app.route('/pool/<int:id>/readings/add')
def add_readings_page(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id': id,
        'user_id': session['user_id']
    }
    return render_template('new_reading.html', one_pool = pool.Pool.get_one_pool(data))

@app.route('/pool/<int:id>/readings/add_to_db', methods=['POST'])
def add_reading_db(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id': id,
        'user_id': session['user_id'],
        'free_chlorine': request.form['free_chlorine'],
        'pH': request.form['pH'],
        'temperature': request.form['temperature']
    }
    reading.Reading.add_simple_reading(data)
    return redirect(f"/pool/{id}")
