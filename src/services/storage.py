import json
import os


class StorageManager:
    USER_FILE = "data/users.json"
    FILE_FILE = "data/files.json"

    
    @staticmethod
    def load_users():
        if not os.path.exists(StorageManager.USER_FILE):
            return []

        try:
            with open(StorageManager.USER_FILE, "r") as f:
                return json.load(f)
        except:
            return []

    @staticmethod
    def save_users(users):
        os.makedirs("data", exist_ok=True)

        with open(StorageManager.USER_FILE, "w") as f:
            json.dump(users, f, indent=4)

   
    @staticmethod
    def load_files():
        if not os.path.exists(StorageManager.FILE_FILE):
            return []

        try:
            with open(StorageManager.FILE_FILE, "r") as f:
                return json.load(f)
        except:
            return []

    @staticmethod
    def save_files(files):
        os.makedirs("data", exist_ok=True)

        with open(StorageManager.FILE_FILE, "w") as f:
            json.dump(files, f, indent=4)