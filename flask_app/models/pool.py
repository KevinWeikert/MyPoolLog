from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import user, reading

class Pool:
    database_schema_name = 'my_pool_log' # Insert Database Schema Name

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.street_address = data['street_address']
        self.city = data['city']
        self.state = data['state']
        self.zipcode = data['zipcode']
        self.water_volume = data['water_volume']
        self.indoor_outdoor = data['indoor_outdoor']
        self.sanitizer = data['sanitizer']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None
        self.readings = []
        self.staff = []

    # Save Pool to Database
    @classmethod
    def save_pool(cls, data):
        query = "INSERT INTO pools (name, street_address, city, state, zipcode, water_volume, indoor_outdoor, sanitizer, user_id) VALUES (%(name)s, %(street_address)s, %(city)s, %(state)s, %(zipcode)s, %(water_volume)s, %(indoor_outdoor)s, %(sanitizer)s, %(user_id)s);"
        return connectToMySQL(cls.database_schema_name).query_db(query, data)

    # Get one Pool
    @classmethod
    def get_one_pool(cls, data):
        query = "SELECT * FROM pools WHERE id = %(id)s;"
        results = connectToMySQL(cls.database_schema_name).query_db(query, data)
        one_pool = cls(results[0])
        return one_pool

    #Get one Pool with all staff
    @classmethod
    def get_one_pool_with_staff(cls,data):
        query = "SELECT * FROM pools LEFT JOIN staffs ON pools.id = staffs.pool_id LEFT JOIN users ON staffs.staff_id = users.id WHERE pools.id=%(id)s"
        results = connectToMySQL(cls.database_schema_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            one_pool = cls(results[0])
            for row_in_db in results:
                staff_data = {
                    'id': row_in_db['users.id'],
                    'first_name': row_in_db['first_name'],
                    'last_name': row_in_db['last_name'],
                    'email': row_in_db['email'],
                    'password': row_in_db['password'],
                    'phone': row_in_db['phone'],
                    'terms_of_service': row_in_db['terms_of_service'],
                    'admin': row_in_db['admin'],
                    'created_at': row_in_db['users.created_at'],
                    'updated_at': row_in_db['users.updated_at']
                }
                one_staff = user.User(staff_data)
                one_pool.staff.append(one_staff)
        return one_pool

    # Get one pool with staff AJAX
    @classmethod
    def get_one_pool_staff_ajax(cls, data):
        query = "SELECT * FROM pools LEFT JOIN staffs ON pools.id = staffs.pool_id LEFT JOIN users ON staffs.staff_id = users.id WHERE pools.id=%(id)s;"
        return connectToMySQL(cls.database_schema_name).query_db(query, data)

    # Get one Pool with all readings
    @classmethod
    def get_one_pool_with_all_readings(cls, data):
        query= "SELECT * FROM pools LEFT JOIN readings ON pools.id = readings.pool_id LEFT JOIN users ON readings.user_id = users.id WHERE pools.id = %(id)s ORDER BY readings.created_at DESC LIMIT 10;"
        results = connectToMySQL(cls.database_schema_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            this_pool = cls(results[0])
            for row_in_db  in results:
                user_data = {
                    'id': row_in_db['users.id'],
                    'first_name': row_in_db['first_name'],
                    'last_name': row_in_db['last_name'],
                    'email': row_in_db['email'],
                    'password': row_in_db['password'],
                    'phone': row_in_db['phone'],
                    'terms_of_service': row_in_db['terms_of_service'],
                    'admin': row_in_db['admin'],
                    'created_at': row_in_db['users.created_at'],
                    'updated_at': row_in_db['users.updated_at']
                }
                user_that_made_reading = user.User(user_data)
                reading_data = {
                    'id': row_in_db['readings.id'],
                    'free_chlorine': row_in_db['free_chlorine'],
                    'pH': row_in_db['pH'],
                    'temperature': row_in_db['temperature'],
                    'total_chlorine': row_in_db['total_chlorine'],
                    'calcium': row_in_db['calcium'],
                    'alkalinity': row_in_db['alkalinity'],
                    'water_volume': row_in_db['water_volume'],
                    'combined_chlorine': row_in_db['combined_chlorine'],
                    'TDS': row_in_db['TDS'],
                    'saturation_index': row_in_db['saturation_index'],
                    'created_at': row_in_db['readings.created_at'],
                    'updated_at': row_in_db['readings.updated_at'],
                    'user_id': row_in_db['user_id'],
                    'pool_id': row_in_db['pool_id'],
                    'user': user_that_made_reading
                }
                one_reading = reading.Reading(reading_data)
                one_reading.user = user_that_made_reading
                this_pool.readings.append(one_reading)
            print(this_pool.readings[1].user)
            return this_pool

    @classmethod
    def edit_pool(cls, data):
        query = "UPDATE pools SET name=%(name)s, street_address=%(street_address)s, city=%(city)s, state=%(state)s, zipcode=%(zipcode)s, water_volume=%(water_volume)s, indoor_outdoor=%(indoor_outdoor)s, sanitizer=%(sanitizer)s WHERE pools.id=id"
        return connectToMySQL(cls.database_schema_name).query_db(query, data)

    # Validations for adding and Updating a Pool
    @staticmethod
    def validate_pool(form_data):
        is_valid = True
        # Pool NAME must be at least 2 characters
        if len(form_data['name']) < 2:
            flash("Pool Name must be at least 2 characters")
            is_valid = False
        # Pool ADDRESS must be at least 5 characters
        if len(form_data['street_address']) < 5:
            flash("Address must be at least 5 characters")
            is_valid = False
        # Pool CITY must be at least 2 characters
        if len(form_data['city']) < 2:
            flash("City must be at least 2 characters")
            is_valid = False
        # Pool STATE must be selected
        if form_data['state'] == "No State Selected":
            flash("Select a State")
            is_valid = False
        # Pool ZIPCODE must be at least 5 characters and a number
        if len(form_data['zipcode']) != 5:
            flash("Please enter a 5 digit zipcode")
            is_valid = False
        # Pool WATER VOLUME must be greater than zero
        if form_data['water_volume'] == '' or int(form_data['water_volume']) < 0:
            flash("Enter water volume greater than 0")
            is_valid = False
        # Pool INDOOR OR OUTDOOR must be selected
        if 'indoor_outdoor' not in form_data:
            flash("Please select if your pool is indoor or outdoor")
            is_valid = False
        # Pool SANITIZER must be selected
        if form_data['sanitizer'] == "Select Sanitizer":
            flash("Select a Sanitizer")
            is_valid = False
        return is_valid