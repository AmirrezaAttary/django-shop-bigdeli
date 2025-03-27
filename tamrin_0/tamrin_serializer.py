from rest_framework import serializers
import re

def validate_national_code(value):
    if not re.match(r'^[0-9]{10}$', value):
        raise serializers.ValidationError("کد ملی باید دقیقا ۱۰ رقم باشد.")
    
    check = int(value[9])
    s = sum(int(value[i]) * (10 - i) for i in range(9)) % 11
    if not (check == s if s < 2 else check == 11 - s):
        raise serializers.ValidationError("کد ملی نامعتبر است.")
    return value

class UserInfoSerializer(serializers.Serializer):
    # شماره موبایل با regex
    phone_number = serializers.RegexField(
        regex=r'^\+9891[0-9]{8}$',
        error_messages={'invalid': "فرمت شماره موبایل صحیح نیست. مثال: +989123456789"}
    )

    
    national_code = serializers.CharField(validators=[validate_national_code])

    
    name = serializers.RegexField(
        regex=r'^[آ-ی\s]+$',
        error_messages={'invalid': "نام فقط باید شامل حروف فارسی باشد."}
    )
