from stores import StudentStore, AttendanceStore
from auth import sign_up, login


def initial_options():
    print("\n------Options------")
    print("1. Signup")
    print("2. Login")
    print("3. Exit")
def logged_in_options():
    print("\n------Options------")
    print("1. Mark Absent for Today")
    print("2. View Attendance History")
    print("3. Correct Attendance")
    print("4. View Attendance Summary")
    print("5. Logout")

def main():

    student_store = StudentStore('data/students.json')
    attendance_store = AttendanceStore('data/attendance.json')

    while True:
        initial_options()
        choice = input("Select an option (1-3): ")
        if choice == '1':
            print("Signup selected.")  
            sign_up(student_store)
        elif choice == '2':
            print("Login selected.")
            student = login(student_store)
            if not student:
                continue
            print(f"Welcome, {student['student_name']}!")
            while True:
                logged_in_options()
                c = input("Select an option (1-5): ")
                if c == '1':
                    reason = input("Enter the reason for your absence: ")
                    if attendance_store.mark_absent(student["student_id"], reason):
                        print("Absent marked successfully for today.")
                    else:
                        print("You have already marked absent for today.")
                elif c == '2':
                    history = attendance_store.absence_history(student["student_id"])
                    print("\n---- Attendance History ----")
                    if not history:
                        print("No absence records found.")
                    else:
                        print("\n")
                        print(f"Date\t\tReason")
                        print("-------------------------")
                        for absence_record in history:
                            print(f"{absence_record['date']}\t\t{absence_record['reason']}")    
                elif c == '3':
                    date = input("Enter the date to correct ur attendance in (YYYY-MM-DD) format: ")
                    if attendance_store.remove_absent(student["student_id"], date):
                        print("Attendance corrected successfully. Peace")
                    else:
                        print("No absence record found for the given date.")            
                elif c == '4':
                    print("\n---- Attendance Summary ----")
                    records = attendance_store.attendance_summary(student["student_id"])
                    print("\n---------------------------")
                    print(f"Total Working Days    : {records['total_working_days']}")
                    print(f"Present Days          : {records['present_days']}")
                    print(f"Absent Days           : {records['total_absences']}")
                    print(f"Attendance Percentage : {records['attendance_percentage']}")
                    print("\n")
                elif c == '5':
                    print("Logging out...")
                    break

        elif choice == '3':
            print("Exiting the application.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
