import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))
db = client.get_database()

# Delete all slots
db.availability_slots.delete_many({})
print("Deleted all slots.")

mentors = list(db.users.find({"role": "mentor"}))
print(f"Found {len(mentors)} mentors")

for mentor in mentors:
    for _ in range(random.randint(3, 5)):
        days_ahead = random.randint(1, 14)
        hour = random.choice([9, 10, 11, 12, 14, 15, 16, 17])
        slot_time = datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0) + timedelta(days=days_ahead)
        if slot_time < datetime.now():
            slot_time += timedelta(days=1)
        existing = db.availability_slots.find_one({"mentor_id": mentor["_id"], "slot": slot_time})
        if not existing:
            db.availability_slots.insert_one({
                "mentor_id": mentor["_id"],
                "slot": slot_time,
                "is_booked": False
            })
            print(f"Added slot for {mentor['name']}: {slot_time}")
print("Done.")