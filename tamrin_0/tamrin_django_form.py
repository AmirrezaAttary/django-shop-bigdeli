from django import forms
import re
from django.core.exceptions import ValidationError

def validate_national_code(value):
    if not re.match(r'^[0-9]{10}$', value):
        raise ValidationError("کد ملی باید دقیقا ۱۰ رقم باشد.")
    
    check = int(value[9])
    s = sum(int(value[i]) * (10 - i) for i in range(9)) % 11
    if not (check == s if s < 2 else check == 11 - s):
        raise ValidationError("کد ملی نامعتبر است.")


class UserInfoForm(forms.Form):
    
    phone_number = forms.RegexField(
        regex=r'^\+9891[0-9]{8}$',
        label="شماره موبایل",
        error_messages={'invalid': "فرمت شماره موبایل معتبر نیست. مثال: +989123456789"}
    )

    
    national_code = forms.CharField(
        label="کد ملی",
        max_length=10,
        validators=[validate_national_code]
    )

    
    name = forms.RegexField(
        regex=r'^[آ-یA-Za-z\s]+$',
        label="نام",
        error_messages={'invalid': "نام فقط می‌تواند شامل حروف فارسی و فاصله باشد."}
    )
