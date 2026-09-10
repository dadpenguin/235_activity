import random

def generate_random_user_id():
    return generate_random(1000, 9999)

def generate_random_review_id():
    return generate_random(1000, 9999)

def generate_random(min: int, max: int):
    return random.randint(min, max)
