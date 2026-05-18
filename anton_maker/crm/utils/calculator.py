from decimal import Decimal, ROUND_UP

MIN_ORDER_PRICE = Decimal('300.00')
LASER_WEAR_SURCHARGE = Decimal('1.05')  # 5% на износ

def calculate_order_cost(length_cm: float, price_per_unit: float, material_type: str = 'standard') -> Decimal:
    length = Decimal(str(length_cm))
    unit_price = Decimal(str(price_per_unit))
    
    base_cost = length * unit_price
    
    if material_type == 'premium':
        base_cost *= Decimal('1.20')
        
    base_cost *= LASER_WEAR_SURCHARGE
    
    if base_cost < MIN_ORDER_PRICE:
        return MIN_ORDER_PRICE
        
    return base_cost.quantize(Decimal('1'), rounding=ROUND_UP)
