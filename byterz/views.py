# app/views.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from byterz.models import Food, UserSettings, Meal, MealItem, WeightEntry
from byterz.forms import FoodForm, WeightForm, MealItemForm
from byterz import db
from byterz.utils import earth_to_mars_weight, earth_kcal_to_redcal

main_bp = Blueprint("main", __name__, template_folder="templates")

@main_bp.route("/")
def index():
    foods = []
    if current_user.is_authenticated:
        foods = Food.query.order_by(Food.is_mars_food.desc(), Food.name).limit(6).all()
    return render_template("index.html", foods=foods)

@main_bp.route("/foods")
@login_required
def foods():
    q = request.args.get("q", "")
    if q:
        items = Food.query.filter(Food.name.ilike(f"%{q}%")).order_by(Food.is_mars_food.desc()).all()
    else:
        items = Food.query.order_by(Food.is_mars_food.desc(), Food.name).all()
    return render_template("foods.html", foods=items, q=q)

@main_bp.route("/foods/new", methods=["GET","POST"])
@login_required
def food_new():
    form = FoodForm()
    if form.validate_on_submit():
        f = Food(
            name=form.name.data,
            serving_text=form.serving_text.data or "1 serving",
            calories=form.calories.data,
            protein_g=form.protein_g.data or 0.0,
            carbs_g=form.carbs_g.data or 0.0,
            fats_g=form.fats_g.data or 0.0,
            is_mars_food=form.is_mars_food.data,
            created_by=current_user.id
        )
        db.session.add(f)
        db.session.commit()
        flash("Food added", "success")
        return redirect(url_for("main.foods"))
    return render_template("food_edit.html", form=form, new=True)

@main_bp.route("/foods/<int:food_id>/edit", methods=["GET","POST"])
@login_required
def food_edit(food_id):
    f = Food.query.get_or_404(food_id)
    form = FoodForm(obj=f)
    if form.validate_on_submit():
        f.name = form.name.data
        f.serving_text = form.serving_text.data or "1 serving"
        f.calories = form.calories.data
        f.protein_g = form.protein_g.data or 0.0
        f.carbs_g = form.carbs_g.data or 0.0
        f.fats_g = form.fats_g.data or 0.0
        f.is_mars_food = form.is_mars_food.data
        db.session.commit()
        flash("Food updated", "success")
        return redirect(url_for("main.foods"))
    return render_template("food_edit.html", form=form, new=False, food=f)

@main_bp.route("/weight", methods=["GET","POST"])
@login_required
def weight():
    form = WeightForm()
    if form.validate_on_submit():
        unit = request.form.get("unit", "kg")
        w = form.weight.data
        # convert to kg if necessary
        kg = w * 0.45359237 if unit == "lb" else w
        entry = WeightEntry(user_id=current_user.id, weight=kg)
        db.session.add(entry)
        db.session.commit()
        flash("Weight saved", "success")
        return redirect(url_for("main.weight"))

    # fetch all weight entries for the current user
    weights = WeightEntry.query.filter_by(user_id=current_user.id).order_by(WeightEntry.created_at).all()
    labels = [w.created_at.strftime("%Y-%m-%d") for w in weights]
    values = [round(w.weight, 2) for w in weights]

    last = weights[-1] if weights else None

    return render_template("weight.html", form=form, last=last, labels=labels, values=values)

@main_bp.route("/api/convert/weight")
@login_required
def api_convert_weight():
    try:
        v = float(request.args.get("value"))
    except:
        return jsonify({"error":"value required"}), 400
    unit = request.args.get("unit", "kg")
    mars = earth_to_mars_weight(v, unit=unit)
    return jsonify({"earth": v, "mars": mars, "unit": unit})

# @main_bp.route("/diary", methods=["GET","POST"])
# @login_required

@main_bp.route("/meal/log", methods=["GET","POST"])
@login_required
def meal_log():
    form = MealItemForm()
    foods = Food.query.order_by(Food.is_mars_food.desc(), Food.name).all()

    if request.method == "POST" and form.validate_on_submit():
        food_id = int(form.food_id.data)
        qty = form.qty.data or 1.0
        meal_name = request.form.get("meal_name")  # <-- get selected meal
        food = Food.query.get_or_404(food_id)
        calories = round(food.calories * qty, 1)

        # Get or create the meal for this user
        meal = Meal.query.filter_by(user_id=current_user.id, name=meal_name).first()
        if not meal:
            meal = Meal(user_id=current_user.id, name=meal_name)
            db.session.add(meal)
            db.session.commit()

        # Add food to meal
        mi = MealItem(meal_id=meal.id, food_id=food.id, qty=qty, calories=calories)
        db.session.add(mi)
        db.session.commit()

        flash(f"Logged {food.name} to {meal_name.capitalize()} ({calories} kcal)", "success")

    return render_template("meal_log.html", form=form, foods=foods)

MEALS = ["breakfast", "lunch", "dinner", "snack"]
@main_bp.route('/diary', methods=['GET'])
@login_required
def diary():
    foods = Food.query.all()
    diary_meals = {}

    for meal_name in MEALS:
        meal = Meal.query.filter_by(user_id=current_user.id, name=meal_name).first()
        if not meal:
            meal = Meal(user_id=current_user.id, name=meal_name)
            db.session.add(meal)
            db.session.commit()
        diary_meals[meal_name] = MealItem.query.filter_by(meal_id=meal.id).all()

    return render_template("diary.html", foods=foods, diary=diary_meals)

@main_bp.route('/diary/add/<meal_name>', methods=['POST'])
@login_required
def add_food(meal_name):
    food_id = int(request.form.get("food_id"))
    qty = float(request.form.get("quantity"))

    # Get the Meal for this user and meal_name
    meal = Meal.query.filter_by(user_id=current_user.id, name=meal_name).first()
    if not meal:
        meal = Meal(user_id=current_user.id, name=meal_name)
        db.session.add(meal)
        db.session.commit()

    food = Food.query.get(food_id)
    if not food:
        return "Food not found", 404

    # Cache calories based on qty
    calories = food.calories * qty

    item = MealItem(meal_id=meal.id, food_id=food.id, qty=qty, calories=calories)
    db.session.add(item)
    db.session.commit()

    return redirect(url_for("main.diary"))