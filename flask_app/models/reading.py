from unicodedata import category
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from decimal import Decimal
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
        self.combined_chlorine = data['combined_chlorine']
        self.TDS = data['TDS']
        self.saturation_index = data['saturation_index']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.pool_id = data['pool_id']
        self.pool = None
        self.user = None
    
    # Add Simple Reading to Database
    @classmethod
    def add_simple_reading(cls, data):
        query = "INSERT INTO readings (free_chlorine, pH, temperature, user_id, pool_id) VALUES (%(free_chlorine)s, %(pH)s, %(temperature)s, %(user_id)s, %(id)s);"
        return connectToMySQL(cls.database_schema_name).query_db(query, data)

    #Add Advanced Reading to Database
    @classmethod
    def add_advanced_reading(cls, data):
        query = "INSERT INTO readings (free_chlorine, total_chlorine, combined_chlorine, pH, temperature, calcium, alkalinity, TDS, saturation_index, user_id, pool_id) VALUES (%(free_chlorine)s, %(total_chlorine)s, %(combined_chlorine)s, %(pH)s, %(temperature)s,%(calcium)s, %(alkalinity)s, %(TDS)s, %(saturation_index)s, %(user_id)s, %(id)s);"
        return connectToMySQL(cls.database_schema_name).query_db(query, data)

    #Delete Reading from Database
    @classmethod
    def delete_reading(cls, data):
        query = "DELETE FROM readings WHERE readings.id = %(reading_id)s;"
        return connectToMySQL(cls.database_schema_name).query_db(query, data)


# Add readings validations
    @staticmethod
    def validate_simple_reading(form_data):
        is_valid = True
        # Free Chlorine Must be greater than zero
        print(form_data)
        if  form_data['free_chlorine'] == '' or Decimal(form_data['free_chlorine']) < 0:
            flash("Free chorine must be greater than 0 and not blank", "simple")
            is_valid = False
        # pH must be between 0 and 14
        if form_data['pH']== '' or Decimal(form_data['pH'])< 0 or Decimal(form_data['pH']) > 14:
            flash("pH must be between 0-14 and not blank", "simple")
        # Temperature must be between 32 - 105 degrees F
        if form_data['temperature']== '' or Decimal(form_data['temperature'])< 0 or Decimal(form_data['temperature']) > 14:
            flash("Temperature must be between 32-105 degrees F and not blank", "simple")
        return is_valid

    @staticmethod
    def validate_advanced_reading(form_data):
        is_valid = True
        # Free Chlorine Must be greater than zero
        print(form_data)
        if  form_data['free_chlorine'] == '' or Decimal(form_data['free_chlorine']) < 0:
            flash("Free chorine must be greater than 0 and not blank", "advanced")
            is_valid = False
        # Total chlorine must be greater than Free Chlorine
        if form_data['total_chlorine'] == '' or Decimal(form_data['total_chlorine']) < Decimal(form_data['free_chlorine']):
            flash("Total chlorine must be greater than free chlorine and not blank", "advanced")
            is_valid = False
        # pH must be between 0 and 14
        if form_data['pH']== '' or Decimal(form_data['pH'])< 0 or Decimal(form_data['pH']) > 14:
            flash("pH must be between 0-14 and not blank", "advanced")
            is_valid = False
        # Temperature must be between 32 - 105 degrees F
        if form_data['temperature']== '' or Decimal(form_data['temperature']) < 0 or Decimal(form_data['temperature']) > 105:
            flash("Temperature must be between 32-105 degrees F and not blank", "advanced")
            is_valid = False
        # Calcium must be greater than 0
        if form_data['calcium'] == '' or Decimal(form_data['calcium']) < 0:
            flash("Calcium must be great than zero", "advanced")
            is_valid = False
        #Alkalinity must be greater than 0
        if form_data['alkalinity'] == '' or Decimal(form_data['alkalinity']) < 0:
            flash("Alkalinity must be great than zero", "advanced")
            is_valid = False
        # TDS must be greater than 0 and not empty
        if form_data['TDS'] == '' or Decimal(form_data['TDS']) < 0:
            flash("TDS must be great than zero", "advanced")
            is_valid = False
        return is_valid