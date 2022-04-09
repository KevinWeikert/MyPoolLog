from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import user, pool

class Reading:
    database_schema_name = 'my_pool_log' # Insert Database Schema Name

    def __init__(self, data):
        self.id = data['id']
        self.free_chlorine = data['free_chlorine']
        self.pH = data['pH']
        self.temperature = data['temperature']
        self.total_chlorine = data['total_chlorine']
        self.calcium = data['calcium']
        self.alkalinity = data['alkalinity']
        self.water_volume = data['water_volume']
        self.combined_chlorine = data['combined_chlorine']
        self.TDS = data['TDS']
        self.saturation_index = data['saturation_index']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.pool_id = data['pool_id']
        self.pool = None
    
    # Add Reading to Database
    @classmethod
    def add_simple_reading(cls, data):
        query = "INSERT INTO readings (free_chlorine, pH, temperature, user_id, pool_id) VALUES (%(free_chlorine)s, %(pH)s, %(temperature)s, %(user_id)s, %(id)s);"
        return connectToMySQL(cls.database_schema_name).query_db(query, data)


# Add readings validations
