import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

def purify_query(value: str, min_length=2, max_length=40):
    value = value.strip()

    if len(value) < min_length:
        raise ValidationError(f"عبارت باید حداقل {min_length} کاراکتر داشته باشد.")

    if len(value) > max_length:
        raise ValidationError(f"عبارت  باید حداکثر {max_length} کاراکتر داشته باشد.")

    if not re.match(r'^[\w\u0600-\u06FF\s-]+$', value):
        raise ValidationError("کاراکتر غیرمجاز وارد شده است.")

    return value




class ValidField(serializers.CharField):
    def __init__(self, *args, **kwargs):
  
        kwargs['allow_blank'] = kwargs.get('allow_blank', True)
        super().__init__(*args, **kwargs)
    
    def to_internal_value(self, value):

        if value is None or value.strip() == "":
            return value  

        value = super().to_internal_value(value)
        return purify_query(value)

