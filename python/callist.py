
students = {}

while True:
    print("\n1. Add Student")
    print("2. Search Student")
    print("3. Show All Students")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        name = input("Enter student name: ")
        mark = int(input("Enter mark: "))
        students[name] = mark
        print("Student added successfully")

    elif choice == "2":
        name = input("Enter student name to search: ")

        if name in students:
            print("Mark:", students[name])
        else:
            print("Student not found")

    elif choice == "3":
        print("All Students:", students)

    elif choice == "4":
        print("Program ended")
        break

    else:
        print("Invalid choice")


