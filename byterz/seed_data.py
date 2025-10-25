# seed_data.py - creates instance DB and seeds sample foods + demo user
import random
from byterz import create_app, db
from byterz.models import User, Food

app = create_app()
with app.app_context():
    db.create_all()

    # --- Demo user ---
    if not User.query.filter_by(username="demo").first():
        u = User(username="demo")
        u.set_password("demo123")
        db.session.add(u)

    # --- Sample foods ---
    samples = [
        {"name":"Earth Oatmeal","is_mars_food":False,"serving_text":"1 cup","calories":150,"protein_g":5,"carbs_g":27,"fats_g":3},
        {"name":"Grilled Chicken","is_mars_food":False,"serving_text":"100 g","calories":165,"protein_g":31,"carbs_g":0,"fats_g":3.6},
        {"name":"Regolith Granola","is_mars_food":True,"serving_text":"1 bar","calories":200,"protein_g":6,"carbs_g":28,"fats_g":7},
        {"name":"Hydroponic Kale Chips","is_mars_food":True,"serving_text":"30 g","calories":80,"protein_g":3,"carbs_g":8,"fats_g":4},
        {"name":"Aeroponic Protein Bar","is_mars_food":True,"serving_text":"1 bar","calories":240,"protein_g":20,"carbs_g":22,"fats_g":8},
    ]
    for s in samples:
        if not Food.query.filter_by(name=s["name"]).first():
            f = Food(**s)
            db.session.add(f)

    # --- Name pools for random foods ---
    adjectives = ["Spicy", "Crunchy", "Sweet", "Savory", "Tangy", "Smoky", "Glazed", "Roasted", "Frozen", "Hydroponic"]
    mars_prefix = ["Martian", "Red Planet", "Regolith", "Aeroponic", "Hydroponic"]
    food_types = ["Protein Bar", "Snack", "Salad", "Oatmeal", "Chicken", "Granola", "Kale Chips", "Smoothie", "Soup", "Wrap"]

    # --- Generate 500 random foods ---
    for i in range(1, 501):
        is_mars_food = random.choice([True, False])

        # Pick adjectives and type
        adj = random.choice(adjectives)
        food = random.choice(food_types)
        if is_mars_food:
            prefix = random.choice(mars_prefix)
            name = f"{adj} {prefix} {food}"
        else:
            name = f"{adj} {food}"

        serving_text = f"{random.randint(1, 300)} g"
        calories = random.randint(50, 500)
        protein_g = round(random.uniform(0, 50), 1)
        carbs_g = round(random.uniform(0, 100), 1)
        fats_g = round(random.uniform(0, 30), 1)

        # Only add if name doesn't exist
        if not Food.query.filter_by(name=name).first():
            f = Food(
                name=name,
                is_mars_food=is_mars_food,
                serving_text=serving_text,
                calories=calories,
                protein_g=protein_g,
                carbs_g=carbs_g,
                fats_g=fats_g
            )
            db.session.add(f)

    db.session.commit()
    print("Seed complete. Demo user: demo / demo123, plus 500 realistic foods")