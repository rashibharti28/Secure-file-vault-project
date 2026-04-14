class AuditLogger:
    @staticmethod
    def log(user, action, filename):
        print(f"[LOG] {user.username} performed {action} on {filename}")