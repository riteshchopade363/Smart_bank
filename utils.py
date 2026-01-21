import random

def generate_otp():
    return random.randint(100000, 999999)

def generate_account_no():
    return "SB" + str(random.randint(10000000, 99999999))
