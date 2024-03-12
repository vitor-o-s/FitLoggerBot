from pymongo import MongoClient
from datetime import datetime

CONNECTION_STRING = ''


# def get_database():
    
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    # db = MongoClient(CONNECTION_STRING)["workout_log"]

    # Selecionar a coleção
    # collection = db["workouts"]

    # return collection

def save_workout(exercise_name: str, reps: int, weight: float, load: float, user_id: int):
    working_set = {
        'user': user_id,
        'exercise': exercise_name,
        'reps': reps,
        'weight': weight,
        'load': load,
        'date': datetime.now()
    }

    collection = MongoClient(CONNECTION_STRING)["workout_log"]["workouts"]
    return collection.insert_one(working_set)




# This is added so that many files can reuse the function get_database()
# if __name__ == '__main__':
    
    # Get the database
    #dbname = get_database()
