import re

def validate_username(username):
    return re.match(r'^[a-zA-Z0-9]{3,}$', username) is not None

def validate_password(password):
    return re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password) is not None

def validate_post_content(content):
   return len(content) >= 10

def validate_phone_number(phone_number):
    return re.match(r'^\d{10,15}$', phone_number) is not None

def validate_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

