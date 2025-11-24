"""
Benchmark: Complex Spaghetti Code

Expected Issues:
- High cyclomatic complexity (Grade F)
- Poor code organization
- No error handling
- PEP 8 violations
"""


def process_order(order_id, user_id, items, discount_code, shipping_method, payment_method, gift_wrap, priority, notes):
    """
    QUALITY ISSUE: High cyclomatic complexity
    McCabe complexity > 20 (Grade F)
    """
    total = 0
    shipping_cost = 0
    discount = 0
    
    # Calculate item total
    for item in items:
        if item['category'] == 'electronics':
            if item['price'] > 1000:
                if user_id in get_premium_users():
                    total += item['price'] * 0.9
                else:
                    total += item['price']
            else:
                total += item['price']
        elif item['category'] == 'clothing':
            if item['on_sale']:
                if item['discount_percent'] > 20:
                    total += item['price'] * 0.7
                else:
                    total += item['price'] * 0.85
            else:
                total += item['price']
        elif item['category'] == 'books':
            if len(items) > 3:
                total += item['price'] * 0.95
            else:
                total += item['price']
        else:
            total += item['price']
    
    # Calculate shipping
    if shipping_method == 'express':
        if total > 100:
            shipping_cost = 15
        else:
            shipping_cost = 25
    elif shipping_method == 'standard':
        if total > 50:
            shipping_cost = 5
        else:
            shipping_cost = 10
    elif shipping_method == 'economy':
        shipping_cost = 0
    
    # Apply discount
    if discount_code:
        if discount_code == 'SAVE10':
            discount = total * 0.1
        elif discount_code == 'SAVE20':
            discount = total * 0.2
        elif discount_code == 'VIP':
            if user_id in get_premium_users():
                discount = total * 0.3
            else:
                discount = total * 0.15
    
    # Gift wrap
    if gift_wrap:
        if total > 100:
            shipping_cost += 5
        else:
            shipping_cost += 10
    
    # Priority processing
    if priority:
        if shipping_method == 'express':
            shipping_cost += 20
        elif shipping_method == 'standard':
            shipping_cost += 10
    
    final_total = total - discount + shipping_cost
    
    # Payment processing (no error handling)
    if payment_method == 'credit_card':
        process_credit_card(final_total)
    elif payment_method == 'paypal':
        process_paypal(final_total)
    elif payment_method == 'bitcoin':
        process_bitcoin(final_total)
    
    return final_total


def get_premium_users():
    return [1, 2, 3]


def process_credit_card(amount):
    pass


def process_paypal(amount):
    pass


def process_bitcoin(amount):
    pass
