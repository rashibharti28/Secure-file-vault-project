from src.services.vault import VaultSystem
from src.services.auth import AuthService
from src.utils.file_handler import FileHandler

vault = VaultSystem()
auth = AuthService()

current_user = None


def auth_menu():
    print("\n" + "="*40)
    print("🔐 Secure File Vault")
    print("="*40)
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    print("="*40)


def vault_menu(user):
    print("\n" + "="*40)
    print(f"👤 Logged in as: {user.username}")
    print("="*40)
    print("1. Upload File")
    print("2. Download File")
    print("3. View My Files")
    print("4. Edit File")
    print("5. Logout")
    print("="*40)


def upload_menu():
    print("\nChoose upload method:")
    print("1. Write content manually")
    print("2. Upload from file path")



def main():
    global current_user

    while True:
        if not current_user:
            auth_menu()
            choice = input("Select option: ").strip()

            if choice == "1":
                username = input("Enter username: ")
                password = input("Enter password: ")
                auth.register(username, password)

            elif choice == "2":
                username = input("Enter username: ")
                password = input("Enter password: ")
                user = auth.login(username, password)
                if user:
                    current_user = user

            elif choice == "3":
                print("👋 Exiting...")
                break

            else:
                print("❌ Invalid choice")

        else:
            vault_menu(current_user)
            choice = input("Select option: ").strip()

            if choice == "1":
                upload_menu()
                method = input("Choose option: ").strip()

                if method == "1":
                    filename = input("Enter filename: ")
                    data = input("Enter content: ")
                    vault.upload_file(current_user, filename, data)

                elif method == "2":
                    filepath = input("Enter file path: ").strip()
                    filename, data = FileHandler.read_file(filepath)

                    if filename and data:
                              vault.upload_file(current_user, filename, data)
                else:
                    print("❌ Invalid option")

                    

                

            elif choice == "2":
                filename = input("Enter filename: ")
                vault.download_file(current_user, filename)

            elif choice == "3":
                vault.list_files(current_user)
            
            elif choice == "4":
               filename = input("Enter filename to edit: ")
               vault.edit_file(current_user, filename)


            elif choice == "5":
                current_user = None
                print("🔓 Logged out")

            else:
                print("❌ Invalid choice")


if __name__ == "__main__":
    main()