# app/models.py
from datetime import datetime
from byterz import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    settings = db.relationship("UserSettings", uselist=False, backref="user")
    weights = db.relationship("WeightEntry", backref="user", lazy=True)
    meals = db.relationship("Meal", backref="user", lazy=True)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

class UserSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    unit = db.Column(db.String(8), default="kg")  # "kg" or "lb"
    redcal_factor = db.Column(db.Float, default=0.9)  # conversion factor RedCal = kcal * factor

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    is_mars_food = db.Column(db.Boolean, default=False)
    serving_text = db.Column(db.String(80), default="1 serving")
    calories = db.Column(db.Float, nullable=False)  # Earth kcal per serving
    protein_g = db.Column(db.Float, default=0.0)
    carbs_g = db.Column(db.Float, default=0.0)
    fats_g = db.Column(db.Float, default=0.0)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), default="Meal")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship("MealItem", backref="meal", lazy=True)

    def total_calories(self):
        return sum(item.calories for item in self.items)

class MealItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey("meal.id"), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey("food.id"), nullable=False)
    qty = db.Column(db.Float, default=1.0)  # multiplier
    calories = db.Column(db.Float, nullable=False)  # cached Earth kcal
    food = db.relationship("Food", backref="meal_items", lazy=True)

class WeightEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    weight = db.Column(db.Float, nullable=False)  # stored in kg
    created_at = db.Column(db.DateTime, default=datetime.utcnow)