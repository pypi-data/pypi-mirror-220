import random, string

def random_string(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for _ in range(length))