from datetime import datetime
import random
from string import ascii_uppercase

def get_current_datetime():
    datetime_string = datetime_string = datetime.now().strftime("%Y-%m-%d||%H:%M:%S")
    return datetime_string

rooms = {}

def generate_room_code(length):
    code = ""
    for i in range(length):
        code = code + random.choice(ascii_uppercase)

    if code in rooms:
        generate_room_code(length)
    else:
        return code