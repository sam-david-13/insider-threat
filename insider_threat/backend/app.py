from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import datetime
import random

app = Flask(__name__)
CORS(app)

# ============================
# 🔗 MongoDB CONNECTION
# ============================
client = MongoClient(
    "mongodb+srv://samdavid13032007_db_user:samdavid@cluster0.kfsohpz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
db = client["insiderDB"]

users_col = db["users"]
logs_col = db["activity_logs"]
anomalies_col = db["anomalies"]

# ============================
# 🧠 ROUTES
# ============================

@app.route('/')
def home():
    return jsonify({"message": "Insider Threat Detection API Running"})

# ✅ GET all users
@app.route('/api/users', methods=['GET'])
def get_users():
    users = list(users_col.find({}, {"_id": 0}))
    return jsonify(users)

# ✅ ADD new user
@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    data["created_at"] = datetime.datetime.now().isoformat()
    users_col.insert_one(data)
    return jsonify({"message": "User added successfully"}), 201

# ✅ LOG user activity
@app.route('/api/activity', methods=['POST'])
def log_activity():
    data = request.json
    data["timestamp"] = datetime.datetime.now().isoformat()
    logs_col.insert_one(data)
    return jsonify({"message": "Activity logged"})


# ✅ CONFIDENTIAL FILE ACCESS SIMULATION
@app.route('/api/confidential_files', methods=['POST'])
def confidential_access():
    data = request.json
    user_id = data.get("user_id")

    # Randomly allow or deny access
    allowed = random.choice([True, False, False])
    file_name = random.choice([
        "Project_Phoenix_Specs.pdf",
        "Q3_Financial_Data.xlsx",
        "Top_Secret_User_List.db"
    ])
    status = "SUCCESS" if allowed else "DENIED"
    message = f"User {user_id} attempted to access {file_name}. Access {status}."

    # Log the action
    logs_col.insert_one({
        "user_id": user_id,
        "activity": message,
        "timestamp": datetime.datetime.now().isoformat()
    })

    return jsonify({
        "user_id": user_id,
        "file_name": file_name,
        "access_status": status,
        "message": message
    })


# ✅ GET all activity logs
@app.route('/api/activities', methods=['GET'])
def get_all_activities():
    activities = list(logs_col.find({}, {"_id": 0}).sort("timestamp", -1))
    return jsonify(activities)


# ✅ GET all anomalies
@app.route('/api/anomalies', methods=['GET'])
def get_anomalies():
    anomalies = list(anomalies_col.find({}, {"_id": 0}))
    return jsonify(anomalies)


# ✅ Analyze user (Generate threat score)
@app.route('/api/analyze', methods=['POST'])
def analyze_user():
    data = request.json
    user_id = data.get("user_id")

    # Random threat score (0–100%)
    threat_score = random.randint(1, 100)

    anomalies_col.insert_one({
        "user_id": user_id,
        "threat_score": threat_score,
        "reason": random.choice([
            "Multiple failed logins",
            "Suspicious file access",
            "Unusual activity pattern"
        ]),
        "timestamp": datetime.datetime.now().isoformat()
    })

    return jsonify({
        "user_id": user_id,
        "threat_score": threat_score
    })


# ============================
# 🚀 MAIN
# ============================
if __name__ == '__main__':
    app.run(debug=True)
