from utils import load_json, save_json
import hashlib
from getpass import getpass
import os
import uuid
from datetime import datetime

def _hash_password(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

def sign_up(student_store):
    print("\n--- Signup ---")
    usn = input("Enter USN: ")
    if not usn:
        print("USN cannot be empty. Signup failed.")
        return
    
    if student_store.find_student_by_usn(usn):
        print("USN already exists. Please select login.")
        return
    
    student = input("Enter Student name: ")
    if not student:
        print("Student name cannot be empty. Signup failed.")
        return
    
    password = getpass("Enter Password: ")
    if not password:
        print("Password cannot be empty. Signup failed.")
        return
    confirm_password = getpass("Confirm Password: ")
    if password != confirm_password:
        print("Passwords do not match. Signup failed.")
        return
    if(len(password) < 6):
        print("Password must be at least 6 characters long. Signup failed.")
        return
    salt = os.urandom(16)
    hashed_password = _hash_password(password, salt)

    student = {
        "student_id":uuid.uuid4().hex,
        "usn": usn,
        "student_name": student,
        "password_hash": hashed_password.hex(),
        "salt": salt.hex(),
        "created_at": datetime.now().isoformat(),
    }

    student_store.add_student(student)
    print("Signup successful. You can now login.")
    return

def login(student_store):
    print("\n--- Login ---")
    usn = input("Enter USN: ")
    if not usn:
        print("USN cannot be empty. Login failed.")
        return None
    
    student = student_store.find_student_by_usn(usn)
    if not student:
        print("USN not found. Login failed.")
        return None
    
    password = getpass("Enter Password: ")
    salt = bytes.fromhex(student["salt"])  
    hashed_password = _hash_password(password, salt).hex()


    if hashed_password != student['password_hash']:
        print("Incorrect password. Please try again.")
        return None

    print("Welcome, {}!".format(student['student_name']))
    return student
