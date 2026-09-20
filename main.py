import re
with open("input.txt", "r") as file:
    text = file.read()
emails = re.findall(r"[\w.-]+@[\w.-]+\.\w+", text)
unique_emails = list(dict.fromkeys(emails))
for email in unique_emails:
    print(email)
with open("emails.txt", "w") as file:
    for email in unique_emails:
        file.write(email + "\n")
print(f"\n{len(unique_emails)} email addresses extracted successfully.")
print("Saved to emails.txt")
