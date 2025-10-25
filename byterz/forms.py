# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Optional, NumberRange

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=80)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=80)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

class FoodForm(FlaskForm):
    name = StringField("Food name", validators=[DataRequired(), Length(max=200)])
    serving_text = StringField("Serving text", validators=[Optional(), Length(max=80)])
    calories = FloatField("Calories (kcal)", validators=[DataRequired(), NumberRange(min=0)])
    protein_g = FloatField("Protein (g)", validators=[Optional()])
    carbs_g = FloatField("Carbs (g)", validators=[Optional()])
    fats_g = FloatField("Fats (g)", validators=[Optional()])
    is_mars_food = BooleanField("Mars Food?")
    submit = SubmitField("Save")

class WeightForm(FlaskForm):
    weight = FloatField("Weight", validators=[DataRequired(), NumberRange(min=0)])
    unit = StringField("Unit", default="kg")
    submit = SubmitField("Save")

class MealItemForm(FlaskForm):
    food_id = StringField("Food ID", validators=[DataRequired()])
    qty = FloatField("Quantity (servings)", default=1.0, validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField("Add")