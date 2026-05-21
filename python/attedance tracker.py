# Attendance Tracker

students = ["Arun", "Bala", "Charan", "Divya", "Eswar"]

present_count = []
absent_count = []

print("=== ATTENDANCE MARKING SYSTEM ===\n")

for student in students:
    print("Student:", student)
    status = input("Enter P for Present / A for Absent: ").upper()

    if status == "P":
        print("Marked Present\n")
        present_count.append(1)   # increase present count
        absent_count.append(0)
    elif status == "A":
        print("Marked Absent\n")
        present_count.append(0)
        absent_count.append(1)    # increase absent count
    else:
        print("Invalid input, marked Absent by default\n")
        present_count.append(0)
        absent_count.append(1)

# Final results
total_present = sum(present_count)
total_absent = sum(absent_count)

print("=== FINAL ATTENDANCE REPORT ===")
print("Total Students:", len(students))
print("Present:", total_present)
print("Absent:", total_absent)
