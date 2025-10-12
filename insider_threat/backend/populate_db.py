from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# ---------------------------
# Database Connection
# ---------------------------
MONGO_URI = "mongodb+srv://samdavid13032007_db_user:samdavid@cluster0.kfsohpz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["cyber_security"]
employees_col = db["employees"]
activity_logs_col = db["activity_logs"]

# ---------------------------
# Sample Data
# ---------------------------
first_names = ["John", "Emma", "Liam", "Olivia", "Noah", "Sophia", "James", "Ava", "Lucas", "Mia", "Ethan", "Amelia", "Aiden", "Harper", "Mason", "Ella", "Logan", "Grace", "Elijah", "Chloe"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
departments = ["IT", "Finance", "HR", "R&D", "Marketing", "Support"]
roles = ["Engineer", "Analyst", "Manager", "Intern", "Consultant"]

# ---------------------------
# Generate 50 Employees
# ---------------------------
employees = []
for i in range(1, 51):
    emp_id = f"E{i:03d}"
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    department = random.choice(departments)
    role = random.choice(roles)
    threat_score = round(random.uniform(0, 100), 2)  # percentage

    employees.append({
        "_id": emp_id,
        "name": name,
        "department": department,
        "role": role,
        "threat_score": threat_score
    })

# Clear old data and insert new
employees_col.delete_many({})
employees_col.insert_many(employees)
print("✅ 50 employees inserted successfully!")

# ---------------------------
# Generate Activity Logs
# ---------------------------
activity_types = ["Login", "File Access", "File Download", "USB Inserted", "Network Request", "Privilege Escalation", "Suspicious Command"]

def generate_random_log(emp_id):
    activity = random.choice(activity_types)
    time_offset = random.randint(0, 10 * 24 * 60)  # past 10 days in minutes
    timestamp = datetime.now() - timedelta(minutes=time_offset)
    severity = random.choice(["Low", "Medium", "High"])
    details = f"{activity} detected for {emp_id} with {severity} severity."

    return {
        "emp_id": emp_id,
        "activity": activity,
        "severity": severity,
        "details": details,
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")
    }

activity_logs = []
for emp in employees:
    num_logs = random.randint(5, 15)  # logs per employee
    for _ in range(num_logs):
        log = generate_random_log(emp["_id"])
        activity_logs.append(log)

activity_logs_col.delete_many({})
activity_logs_col.insert_many(activity_logs)
print(f"✅ {len(activity_logs)} activity logs inserted successfully!")
print("Database population complete 🎯")
