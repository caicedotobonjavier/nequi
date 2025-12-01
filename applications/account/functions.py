#
import string
#
import secrets

def number(size=20, chars=string.digits):
    number=[]
    for _ in range(0, size):
        number.append(secrets.choice(chars))
    return ''.join(number)