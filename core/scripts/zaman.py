def save_work_times_to_file(input_str, filename="work_times.txt"):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(input_str.strip() + "\n---\n")  # "---" برای جدا کردن روزها

# Example usage:
input_data = """
10:23
13:21
14:47
17:01
"""
save_work_times_to_file(input_data)
print("Work times saved to file.")
