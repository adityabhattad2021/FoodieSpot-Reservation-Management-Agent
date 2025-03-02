import random
import string

def generate_reservation_code(length=6):
    """Generate a random alphanumeric code for reservations"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))