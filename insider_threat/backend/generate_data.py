from pymongo import MongoClient
import random
import datetime

client = MongoClient("mongodb+srv://samdavid13032007_db_user:samdavid@cluster0.kfsohpz.mongodb.net/?retryWrites=true&w=majority")
db = client["insiderDB"]
users = list(db.users.find({}, {"id":1, "_id":0}))

activities = [
    "Logged in", "Logged out", "Downloaded file", "Uploaded file",
    "Accessed confidential report", "Sent email", "Modified database record",
    "Failed login attempt", "Changed password", "Connected USB device"
]

for user in users:
    for _ in range(random.randint(5, 15)):  # 5-15 logs per user
        db.activity_logs.insert_one({
            "user_id": user["id"],
            "activity": random.choice(activities),
            "timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=random.randint(0,10000))).isoformat()
        })

print("Activity logs generated!")
