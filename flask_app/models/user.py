from multiprocessing import pool
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
from flask_bcrypt import Bcrypt
from flask_app.models import pool
bcrypt = Bcrypt(app)
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    database_schema_name = 'my_pool_log' # Insert Database Schema Name

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.phone = data['phone']
        self.terms_of_service = data['terms_of_service']
        self.admin = data['admin']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pools = []

    # Save New Admin User
    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, terms_of_service) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(terms_of_service)s);"
        return connectToMySQL(cls.database_schema_name).query_db(query, data)

    # Save New Staff User
    @classmethod
    def save_staff_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, admin) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(admin)s);"
        new_staff = connectToMySQL(cls.database_schema_name).query_db(query, data)
        return new_staff

    #Add staff to pool
    def add_staff_pool(data):
        query = "INSERT INTO  staffs (staff_id, pool_id) VALUES (%(staff_id)s, %(pool_id)s);"
        return connectToMySQL('my_pool_log').query_db(query, data)

    #Get all Staff
    @classmethod
    def get_all_staff(cls):
        query = "SELECT * FROM users WHERE admin=0;"
        results = connectToMySQL(cls.database_schema_name).query_db(query)
        if len(results) == 0:
            return None
        all_staff=[]
        for row_in_db in results:
            all_staff.append(cls(row_in_db))
        return all_staff

    #Get one staff will all Pools
    @classmethod
    def get_one_staff_with_pools(cls, data):
        query = "SELECT * FROM users LEFT JOIN staffs ON users.id = staffs.staff_id LEFT JOIN pools ON staffs.pool_id = pools.id WHERE users.id = %(user_id)s;"
        results = results = connectToMySQL(cls.database_schema_name).query_db(query, data)
        print(results)
        if len(results) == 0:
            return None
        else:
            this_staff = cls(results[0])
            for row_in_db in results:
                pool_data = {
                    'id': row_in_db['pools.id'],
                    'name': row_in_db['name'],
                    'street_address': row_in_db['street_address'],
                    'city': row_in_db['city'],
                    'state': row_in_db['state'],
                    'zipcode': row_in_db['zipcode'],
                    'water_volume': row_in_db['water_volume'],
                    'indoor_outdoor': row_in_db['indoor_outdoor'],
                    'sanitizer': row_in_db['sanitizer'],
                    'created_at': row_in_db['pools.created_at'],
                    'updated_at': row_in_db['pools.updated_at'],
                    'user_id': row_in_db['user_id']
                }
                this_staff.pools.append(pool.Pool(pool_data))
            return this_staff
    
    # Get User by email
    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.database_schema_name).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    # Get 1 User by id
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.database_schema_name).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    # Get current user with all pools
    @classmethod
    def user_with_all_pools(cls, data):
        query = "SELECT * FROM users LEFT JOIN pools ON users.id = pools.user_id WHERE users.id = %(user_id)s;"
        results = results = connectToMySQL(cls.database_schema_name).query_db(query, data)
        print(results)
        if len(results) == 0:
            return None
        else:
            this_user = cls(results[0])
            for row_in_db in results:
                pool_data = {
                    'id': row_in_db['pools.id'],
                    'name': row_in_db['name'],
                    'street_address': row_in_db['street_address'],
                    'city': row_in_db['city'],
                    'state': row_in_db['state'],
                    'zipcode': row_in_db['zipcode'],
                    'water_volume': row_in_db['water_volume'],
                    'indoor_outdoor': row_in_db['indoor_outdoor'],
                    'sanitizer': row_in_db['sanitizer'],
                    'created_at': row_in_db['pools.created_at'],
                    'updated_at': row_in_db['pools.updated_at'],
                    'user_id': row_in_db['user_id']
                }
                this_user.pools.append(pool.Pool(pool_data))
            return this_user

    @classmethod
    def edit_profile(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, phone=%(phone)s WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.database_schema_name).query_db(query,data)

    @classmethod
    def change_password(cls, data):
        query = "UPDATE users SET password=%(password)s WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.database_schema_name).query_db(query,data)

    
    @staticmethod
    def validate_user_registration(form_data):
        is_valid = True
        if len(form_data['first_name']) < 3:
            flash("First must be at least 3 characters", "registration")
            is_valid = False
        if len(form_data['last_name']) < 3:
            flash("Last Name must be at least 3 characters", "registration")
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!", "registration")
            is_valid = False
        data = {
            "email": form_data["email"]
        }
        found_user_or_false = User.get_user_by_email(data)
        if found_user_or_false != False:
            is_valid = False
            flash("Email is Already Registered", "registration")
        if len(form_data['password']) < 8:
            flash("Password must be at Least 8 Characters", "registration")
            is_valid = False
        if form_data['password'] != form_data['confirm_password']:
            flash("Passwords Don't Match", "registration")
            is_valid = False
        if 'terms_of_service' not in form_data:
            flash("Must Agree to Terms of Use", "registration")
            is_valid = False
        # if not form_data['agree_terms']:
        #     flash("Must Agree to Terms of Use", "registration")
        #     is_valid = False
        return is_valid

    @staticmethod
    def validate_staff_registration(form_data):
        is_valid = True
        if len(form_data['first_name']) < 3:
            flash("First must be at least 3 characters")
            is_valid = False
        if len(form_data['last_name']) < 3:
            flash("Last Name must be at least 3 characters")
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!")
            is_valid = False
        data = {
            "email": form_data["email"]
        }
        found_user_or_false = User.get_user_by_email(data)
        if found_user_or_false != False:
            is_valid = False
            flash("Email is Already Registered")
        if len(form_data['password']) < 8:
            flash("Password must be at Least 8 Characters")
            is_valid = False
        if form_data['password'] != form_data['confirm_password']:
            flash("Passwords Don't Match", "registration")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_edit_profile(form_data):
        is_valid = True
        if len(form_data['first_name']) < 3:
            flash("First must be at least 3 characters", "edit")
            is_valid = False
        if len(form_data['last_name']) < 3:
            flash("Last Name must be at least 3 characters", "edit")
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!", "edit")
            is_valid = False
        data = {
            "email": form_data["email"]
        }
        found_user_or_false = User.get_user_by_email(data)
        if found_user_or_false.id == session['user_id']:
            is_valid = True
        else:
            if(found_user_or_false != False):
                is_valid = False
                flash("Email is Already Registered", "edit")
        if len(form_data['phone']) < 10:
            flash("Invalid Phone Number", "edit")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_change_password(form_data):
        is_valid = True
        data={
            'id': session['user_id']
        }
        current_user = User.get_user_by_id(data)
        if(form_data['password'] == current_user.password):
            flash("Password cannot be the same as current password", "change_password")
            is_valid = False
        if len(form_data['password']) < 8:
            flash("Password must be at Least 8 Characters", "change_password")
            is_valid = False
        if form_data['password'] != form_data['confirm_password']:
            flash("Passwords Don't Match", "change_password")
            is_valid = False
        return is_valid


    # Static Method to validate user login information. This option is instead of the validation in the route
    # @staticmethod
    # def validate_user_login(data):
    #     is_valid = True
    #     email_data = {
    #         "email": data["email"]
    #     }
    #     found_user_or_false = User.get_by_email(data)
    #     if found_user_or_false == False:
    #         is_valid = False
    #         flash("Invalid Email/Password")
    #         return is_valid
    #     if not bcrypt.check_password_hash(found_user_or_false.password, data['password']):
    #         is_valid = False
    #         flash("Invalid Email/Password")
    #         return is_valid
    #     return is_valid


