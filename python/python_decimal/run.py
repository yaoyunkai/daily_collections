"""


Created at 2023/3/9
"""
import decimal

# Set the precision for decimal calculations
decimal.getcontext().prec = 4

# Define the money values
price = decimal.Decimal('10.99')
tax_rate = decimal.Decimal('0.0875')
discount_rate = decimal.Decimal('0.10')

# Calculate the total price
subtotal = price * decimal.Decimal('1.0')  # No discount
discount = subtotal * discount_rate
subtotal -= discount
tax = subtotal * tax_rate
total = subtotal + tax

# Print the results
print(f"Price: {price:.2f}")
print(f"Discount: {discount:.2f}")
print(f"Subtotal: {subtotal:.2f}")
print(f"Tax: {tax:.2f}")
print(f"Total: {total:.2f}")
