# seed_data.py - creates instance DB and seeds sample foods + demo user
from byterz import create_app, db
from byterz.models import User, Food
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="demo").first():
        u = User(username="demo")
        u.set_password("demo123")
        db.session.add(u)
    # sample foods
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
    db.session.commit()
    print("Seed complete. Demo user: demo / demo123")