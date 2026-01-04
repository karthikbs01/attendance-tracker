import json
from utils import load_json, save_json
from datetime import datetime
import uuid
class StudentStore:
    # student = {
    #     "student_id": student id,
    #     "usn": usn,
    #     "student_name": student name,
    #     "password_hash": hashed password,
    #     "salt": "",
    #     "created_at": 2025-09-02 09:10:00,
    # }
    def __init__(self, path):
        self.path = path
        self.data = load_json(path, default={"students": []})

    def save(self):
        save_json(self.path, self.data)        

    def find_student_by_usn(self, usn):
        for student in self.data["students"]:
            if student["usn"] == usn:
                return student
        return None
    
    def add_student(self, student):
        self.data["students"].append(student)
        self.save()
    
    def find_student_by_id(self, student_id):
        for student in self.data["students"]:
            if student["student_id"] == student_id:
                return student
        return None
    

class AttendanceStore:
# absent_records = {
    #     "attendance_id": "103",
    #     "student_id": "2",
    #     "date": "2025-09-01",
    #     "reason": "sick",
    #     "marked_at": "2025-09-01 09:07:00"
    # }

    def __init__(self, path):
        self.path = path
        self.data = load_json(path, {"absent_records": []})
    
    def save(self):
        save_json(self.path, self.data)
    #1. Mark Absent for today
    def mark_absent(self, student_id, reason):
        today = datetime.now().date().isoformat()
        for data in self.data["absent_records"]:
            if data["student_id"] == student_id and data["date"] == today:
                return False
        absent_record = {
            "attendance_id": uuid.uuid4().hex,
            "student_id": student_id,
            "date": today,
            "reason": reason,
            "marked_at": datetime.now().isoformat()
         }
        self.data["absent_records"].append(absent_record)
        self.save()
        return True
    #3. Correct Attendance
    def remove_absent(self, student_id, date):
        for data in self.data["absent_records"]:
            if data["student_id"] == student_id and data["date"] == date:
                self.data["absent_records"].remove(data)
                self.save()
                return True
        return False

    #2. View Attendance History
    def absence_history(self, student_id):
        absence_list = []
        for data in self.data["absent_records"]:
            if data["student_id"] == student_id:
                absence_list.append(data)
        return absence_list
    

    #4. View Attendance Summary
    def attendance_summary(self, student_id):
        total_working_days = 150
        total_absences = 0
        for data in self.data["absent_records"]:
            if data["student_id"] == student_id:
                total_absences += 1
        present_days = total_working_days - total_absences
        attendance_percentage = (present_days / total_working_days) * 100
        summary_data = {
            "total_working_days": total_working_days,
            "total_absences": total_absences,
            "present_days": present_days,
            "attendance_percentage": attendance_percentage
        }
        return summary_data

    