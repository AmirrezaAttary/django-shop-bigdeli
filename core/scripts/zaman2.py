from datetime import datetime, timedelta

def calculate_daily_hours(time_list):
    times = [datetime.strptime(t.strip(), "%H:%M") for t in time_list if t.strip()]
    if len(times) % 2 != 0:
        raise ValueError("Each day must have an even number of time entries.")
    total = timedelta()
    for i in range(0, len(times), 2):
        total += times[i + 1] - times[i]
    return total

def calculate_total_from_file(filename="work_times.txt"):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    day_blocks = content.strip().split("---")
    total_duration = timedelta()

    for block in day_blocks:
        lines = block.strip().splitlines()
        if lines:
            total_duration += calculate_daily_hours(lines)

    hours = total_duration.seconds // 3600 + total_duration.days * 24
    minutes = (total_duration.seconds % 3600) // 60
    return f"Total work time from file: {hours} hours and {minutes} minutes"

# Example usage:
print(calculate_total_from_file())
