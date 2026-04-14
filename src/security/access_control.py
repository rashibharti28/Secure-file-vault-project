class AccessControl:
    @staticmethod
    def check_permission(user, file):
        return user.role == "admin" or file.owner == user.username