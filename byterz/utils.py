MARS_GRAVITY = 0.376
LB_TO_KG = 0.45359237

def earth_to_mars_weight(earth_weight, unit="kg"):
    """earth_weight numeric in 'kg' or 'lb'. Returns mars weight in same unit (rounded to 2 decimals)."""
    if unit == "lb":
        earth_kg = earth_weight * LB_TO_KG
        mars_kg = earth_kg * MARS_GRAVITY
        return round(mars_kg / LB_TO_KG, 2)
    return round(earth_weight * MARS_GRAVITY, 2)

def mars_to_earth_weight(mars_weight, unit="kg"):
    if unit == "lb":
        mars_kg = mars_weight * LB_TO_KG
        earth_kg = mars_kg / MARS_GRAVITY
        return round(earth_kg / LB_TO_KG, 2)
    return round(mars_weight / MARS_GRAVITY, 2)

def earth_kcal_to_redcal(earth_kcal, redcal_factor=0.9):
    return round(earth_kcal * redcal_factor, 1)

def redcal_to_earth_kcal(redcal, redcal_factor=0.9):
    return round(redcal / redcal_factor, 1)