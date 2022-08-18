import random
import string

def random_id(k=8):
  return ''.join(random.choices(string.ascii_letters+string.digits, k=k))