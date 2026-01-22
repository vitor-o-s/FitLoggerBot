from datetime import datetime
from os import getenv
from pymongo import MongoClient

CONNECTION_STRING = getenv('MONGODB_CONNECTION_STRING', '')


def save_workout(
    exercise_name: str, reps: int, weight: float, load: float, user_id: int
):
    working_set = {
        'user': user_id,
        'exercise': exercise_name,
        'reps': reps,
        'weight': weight,
        'load': load,
        'date': datetime.now(),
    }
    if CONNECTION_STRING:
        collection = MongoClient(CONNECTION_STRING)['workout_log']['workouts']
    else:
        collection = MongoClient()['workout_log']['workouts']
    return collection.insert_one(working_set)
