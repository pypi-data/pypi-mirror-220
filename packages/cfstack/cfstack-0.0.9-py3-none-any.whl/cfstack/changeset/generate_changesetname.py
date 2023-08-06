import random
import string

def generate_changesetname():
    letters = string.digits + string.ascii_letters
    length = random.randint(2, 5)*random.randint(2, 5)
    change_set_name =  ''.join(random.choice(string.ascii_letters) for _ in range(4))+''.join(random.choice(letters) for _ in range(length))
    return change_set_name