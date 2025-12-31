from django import template

register = template.Library()

def indian_format(number):
    """Convert number into Indian numbering format (e.g., 25,00,000.98)"""
    try:
        number = float(number)
        integer_part, decimal_part = f"{number:.2f}".split(".")  # Separate integer and decimal
        integer_part = integer_part[::-1]  # Reverse for easier grouping
        
        # First group of three, then groups of two
        groups = [integer_part[:3]] + [integer_part[i:i+2] for i in range(3, len(integer_part), 2)]
        
        formatted_integer = ",".join(groups)[::-1]  # Reverse back to normal
        
        return f"{formatted_integer}.{decimal_part}"
    
    except (ValueError, TypeError):
        return number  # Return as-is if conversion fails

@register.filter
def indian_number_format(value):
    return indian_format(value)
