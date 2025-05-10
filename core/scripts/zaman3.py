def parse_time(time_str):
    try:
        hour, minute = map(int, time_str.split(':'))
        return hour, minute
    except ValueError:
        print("فرمت نادرست است. لطفاً زمان را به صورت ساعت:دقیقه وارد کنید.")
        return 0, 0

total_hours = 0
total_minutes = 0

while True:
    user_input = input('time : ').strip()
    if user_input.lower() == 'end':
        break

    hours, minutes = parse_time(user_input)
    total_hours += hours
    total_minutes += minutes

# تبدیل دقایق اضافی به ساعت
total_hours += total_minutes // 60
total_minutes %= 60

print(f"مجموع زمان: {total_hours}:{total_minutes:02d}")
