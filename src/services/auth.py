from src.models.user import User
from src.services.storage import StorageManager

class AuthService:
    def __init__(self):
        self.users = []
        self.user_id_counter = 1
        self.load_users()   

    def load_users(self):
       data = StorageManager.load_users()

       for u in data:
       
         user_id = u.get("id", self.user_id_counter)

         user = User(user_id, u["username"], u["password"], u.get("role", "user"))
         self.users.append(user)

         self.user_id_counter = max(self.user_id_counter, user_id + 1)

    def save_users(self):
        data = []

        for user in self.users:
            data.append({
                "id": user.id,
                "username": user.username,
                "password": user.password,
                "role": user.role
            })

        StorageManager.save_users(data)

    def register(self, username, password):
        # check if user exists
        for user in self.users:
            if user.username == username:
                print("❌ Username already exists")
                return None

        user = User(self.user_id_counter, username, password)
        self.users.append(user)
        self.user_id_counter += 1

        self.save_users()  

        print("✅ Registration successful")
        return user

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                print("✅ Login successful")
                return user

        print("❌ Invalid username or password")
        return None