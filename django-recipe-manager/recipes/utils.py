CONVERSION_FACTORS = {
    "gram": {
        "kilogram": 0.001,
        "pound": 0.00220462,
        "ounce": 0.035274,
    },
    "kilogram": {
        "gram": 1000,
        "pound": 2.20462,
        "ounce": 35.274,
    },
    "pound": {
        "gram": 453.592,
        "kilogram": 0.453592,
        "ounce": 16,
    },
    "ounce": {
        "gram": 28.3495,
        "kilogram": 0.0283495,
        "pound": 0.0625,
    },
    "milliliter": {
        "liter": 0.001,
        "gallon": 0.000264172,
        "fluid_ounce": 0.033814,
        "centiliter": 0.1,
    },
    "liter": {
        "milliliter": 1000,
        "gallon": 0.264172,
        "fluid_ounce": 33.814,
        "centiliter": 100,
    },
    "gallon": {
        "liter": 3.78541,
        "milliliter": 3785.41,
        "fluid_ounce": 128,
        "centiliter": 378.541,
    },
    "fluid_ounce": {
        "milliliter": 29.5735,
        "liter": 0.0295735,
        "gallon": 0.0078125,
        "centiliter": 2.95735,
    },
    "centiliter": {
        "milliliter": 10,
        "liter": 0.01,
        "gallon": 0.00264172,
        "fluid_ounce": 0.33814,
    },
    "inch": {
        "centimeter": 2.54,
        "foot": 0.0833333,
        "yard": 0.0277778,
        "mile": 0.0000157828,
        "meter": 0.0254,
        "kilometer": 0.0000254,
    },
    "foot": {
        "inch": 12,
        "yard": 0.333333,
        "mile": 0.000189394,
        "meter": 0.3048,
        "kilometer": 0.0003048,
        "centimeter": 30.48,
    },
    "yard": {
        "inch": 36,
        "foot": 3,
        "mile": 0.000568182,
        "meter": 0.9144,
        "kilometer": 0.0009144,
        "centimeter": 91.44,
    },
    "mile": {
        "inch": 63360,
        "foot": 5280,
        "yard": 1760,
        "meter": 1609.34,
        "kilometer": 1.60934,
        "centimeter": 160934,
    },
    "centimeter": {
        "inch": 0.393701,
        "foot": 0.0328084,
        "yard": 0.0109361,
        "mile": 0.0000062137,
        "meter": 0.01,
        "kilometer": 0.00001,
    },
    "meter": {
        "inch": 39.3701,
        "foot": 3.28084,
        "yard": 1.09361,
        "mile": 0.000621371,
        "centimeter": 100,
        "kilometer": 0.001,
    },
    "kilometer": {
        "inch": 39370.1,
        "foot": 3280.84,
        "yard": 1093.61,
        "mile": 0.621371,
        "centimeter": 100000,
        "meter": 1000,
    },
}


class UnsupportedUnitConvertion(Exception):
    "Raise unsupported units of measurement"
    pass


def convert_measurement(value, from_unit, to_unit, is_price_conversion=False):
    # Return the value if dont need to convert
    if from_unit == to_unit:
        return value

    # Check if the units are supported
    if from_unit in CONVERSION_FACTORS and to_unit in CONVERSION_FACTORS[from_unit]:
        # Calculate the conversion factor and return the value rounded to 5 decimal places.
        factor = CONVERSION_FACTORS[from_unit][to_unit]
        if is_price_conversion:
            return round(value / factor, 5)
        return round(value * factor, 5)
    else:
        # Raise an exception if the units are not supported.
        raise UnsupportedUnitConvertion
