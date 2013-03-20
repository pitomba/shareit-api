import random
import string

def get_new_random_file_name(size=20, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
