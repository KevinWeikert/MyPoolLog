from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash

class Pool:
    database_schema_name = 'MyPoolLog' # Insert Database Schema Name

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