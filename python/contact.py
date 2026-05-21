
contacts = {}

name = input("Enter name: ")
phone = input("Enter phone number: ")

contacts[name] = phone

search = input("Enter name to search: ")

if search in contacts:
    print("Phone Number:", contacts[search])
else:
    print("Contact not found")
