from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models import user, pool, reading

@app.route('/pool/add')
def add_pool_page():
    if 'user_id' not in session:
        return redirect('/')
    states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }
    sanitizers = {
        'Chlorine': 'Chlorine: Tablet, Liquid, or Gas',
        'Salt Water': 'Salt Water Chlorinators',
    }
    data ={
        "user_id": session['user_id']
    }
    return render_template('add_pool.html', states = states, sanitizers = sanitizers, this_user = user.User.user_with_all_pools(data))

@app.route('/add-pool-db', methods=['POST'])
def add_pool_db():
    if not pool.Pool.validate_pool(request.form):
        return redirect ('/pool/add')
    else:
        data = {
            'name': request.form['name'],
            'street_address': request.form['street_address'],
            'city': request.form['city'],
            'state': request.form['state'],
            'zipcode': request.form['zipcode'],
            'water_volume': request.form['water_volume'],
            'indoor_outdoor': request.form['indoor_outdoor'],
            'sanitizer': request.form['sanitizer'],
            'user_id': session['user_id']
        }
        pool.Pool.save_pool(data)
        return redirect('/dashboard')

# Show 1 pool with readings
@app.route('/pool/<int:id>')
def show_pool(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id,
        "user_id": session['user_id']
    }
    return render_template("show_pool.html", this_pool=pool.Pool.get_one_pool_with_all_readings(data), this_user = user.User.user_with_all_pools(data))