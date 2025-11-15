from .views import list_to_sha512
from datetime import datetime
import random
def create_token(data):
    # create token###########################
    char_list = [
        'H', 'e', 'l', 'l', 'o', '!',
        ' ' ',', "*", "@",
        "a", "l" ,"i" ,"e" ,"b" ,"a" ,"d" ,"i",
        "a" , "r" , "m" ,"a", "n", "p" , "a" ,"r", "v", "a" ,"z",
        "k" , "a" , "s" , "h" , "i"
    ]
    now         = datetime.now()
    char_random = str(
        ''.join(str(random.choice(char_list)) for _ in range(13))
    ) + str(now) + data

    token       = list_to_sha512(char_random)

    # create token###########################

    return token