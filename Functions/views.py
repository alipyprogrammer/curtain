from django.shortcuts import render
import hashlib


# Create your views here.
def string_to_list(string):
    try:
        result_list = eval(string)
        if isinstance(result_list, list):
            return result_list
        else:
            raise ValueError("Input is not a valid list string.")
    except Exception as e:
        print("Error:", e)
        return ([])


def list_to_sha512(char_list):
    input_string = ''.join(char_list)

    byte_string = input_string.encode()

    sha512_hash = hashlib.sha512(byte_string)

    hex_digest = sha512_hash.hexdigest()

    return hex_digest