from decimal import Decimal
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
    return render_template('new_reading.html', one_pool = pool.Pool.get_one_pool(data), this_user = user.User.user_with_all_pools(data))

@app.route('/pool/<int:id>/readings/add_simple_to_db', methods=['POST'])
def add_simple_reading_db(id):
    if not reading.Reading.validate_simple_reading(request.form):
        return redirect (f"/pool/{id}/readings/add")
    data={
        'id': id,
        'user_id': session['user_id'],
        'free_chlorine': request.form['free_chlorine'],
        'pH': request.form['pH'],
        'temperature': request.form['temperature']
    }
    reading.Reading.add_simple_reading(data)
    return redirect(f"/pool/{id}")

@app.route('/pool/<int:id>/readings/add_advanced_to_db', methods=['POST'])
def add_advanced_reading_db(id):
    if not reading.Reading.validate_advanced_reading(request.form):
        return redirect (f"/pool/{id}/readings/add")
    # Calculate Combined Chlorine
    combined_chlorine = Decimal(request.form['total_chlorine']) - Decimal(request.form['free_chlorine'])
    # Temperature Factor Dictionary
    temp_factor_dictionary = {
        '32': '0.0',
        '37': '0.1',
        '46': '0.2',
        '53': '0.3',
        '60': '0.4',
        '66': '0.5',
        '76': '0.6',
        '84': '0.7',
        '94': '0.8',
        '105': '0.9'
    }
    # Get Temperature Factor
    for key, val in temp_factor_dictionary.items():
        Tf = 0
        if Decimal(request.form['temperature'])<=Decimal(key):
            Tf = val
            break
    # Calcium Factor Dictionary
    cal_factor_dictionary = {
        '25': '1.0',
        '50': '1.3',
        '75': '1.5',
        '100': '1.6',
        '125': '1.7',
        '150': '1.8',
        '200': '1.9',
        '250': '2.0',
        '300': '2.1',
        '400': '2.2',
        '800': '2.5'
    }
    # Get Calcium Factor
    for key, val in cal_factor_dictionary.items():
        Cf = 0
        if Decimal(request.form['calcium'])<=Decimal(key):
            Cf = val
            break
    # Alkalinity Factor Dictionary
    Al_factor_dictionary = {
        '25': '1.4',
        '50': '1.7',
        '75': '1.9',
        '100': '2.0',
        '125': '2.1',
        '150': '2.2',
        '200': '2.3',
        '250': '2.4',
        '300': '2.5',
        '400': '2.6',
        '800': '2.9'
    }
    # Get Alkalinity Factor
    for key, val in Al_factor_dictionary.items():
        Af = 0
        if Decimal(request.form['alkalinity'])<=Decimal(key):
            Af = val
            break
    # Get TDS Factor
    if Decimal(request.form['TDS']) < 1000:
        TDSf = 12.1
    else:
        TDSf = 12.2
    # Calculation Saturation Index
    SI = Decimal(request.form['pH'])+Decimal(Tf)+Decimal(Cf)+Decimal(Af)-Decimal(TDSf)
    rounded_SI = round(SI,1)
    data={
        'id': id,
        'user_id': session['user_id'],
        'free_chlorine': request.form['free_chlorine'],
        'total_chlorine': request.form['total_chlorine'],
        'combined_chlorine': combined_chlorine,
        'pH': request.form['pH'],
        'temperature': request.form['temperature'],
        'calcium': request.form['calcium'],
        'alkalinity': request.form['alkalinity'],
        'TDS': request.form['TDS'],
        'saturation_index': rounded_SI
    }
    reading.Reading.add_advanced_reading(data)
    return redirect(f"/pool/{id}")

@app.route('/pool/<int:id>/readings/<int:reading_id>/delete')
def delete_reading(id,reading_id):
    if 'user_id' not in session:
        return redirect('/')
    else:
        data={
            'reading_id': reading_id
        }
        reading.Reading.delete_reading(data)
        return redirect(f"/pool/{id}")