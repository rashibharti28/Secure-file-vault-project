from src.models.file import File
from src.security.encryption import EncryptionManager
from src.services.logger import AuditLogger
from src.services.storage import StorageManager
import os
from datetime import datetime
DEBUG = False


class VaultSystem:
    def __init__(self):
        self.files = []
        self.file_counter = 1
        self.load_files_from_storage()

    # ---------------- UPLOAD ----------------
    def upload_file(self, user, filename, data):
        print("\n🔒 Encrypting file...")

        if isinstance(data, str):
            data = data.encode()

        encrypted = EncryptionManager.encrypt(data)

        if DEBUG:
            print("📄 Original:", data[:50])
            print("🔐 Encrypted:", encrypted[:50])

        # ✅ Prevent duplicate file
        for f in self.files:
            if f.filename == filename and f.owner == user.username:
                print("❌ File already exists")
                return

        # Create user folder
        user_folder = f"data/{user.username}"
        os.makedirs(user_folder, exist_ok=True)

        # Save encrypted file
        encrypted_path = f"{user_folder}/{filename}.enc"
        with open(encrypted_path, "wb") as f:
            f.write(encrypted)

        # Save metadata
        file = File(self.file_counter, filename, user.username, encrypted_path)
        self.files.append(file)
        self.file_counter += 1
        file.upload_date = datetime.now().strftime("%d-%m-%Y %H:%M")
        print("✅ File encrypted & stored securely")
        AuditLogger.log(user, "UPLOAD", filename)

        self.save_files()

    # ---------------- DOWNLOAD ----------------
    def download_file(self, user, filename, password):
        for file in self.files:
            if file.filename == filename and file.owner == user.username:

                if password != user.password:
                    with open(file.encrypted_data, "rb") as f:
                        preview = f.read(32)
                    return {"error": "Wrong password", "preview": preview}

                with open(file.encrypted_data, "rb") as f:
                    encrypted_data = f.read()

                decrypted = EncryptionManager.decrypt(encrypted_data)

                return {
                    "success": True,
                    "data": decrypted,
                    "filename": filename
                }

        return {"error": "File not found"}

    # ---------------- READ FILE CONTENT (NEW 🔥) ----------------
    def read_file_content(self, user, filename):
        for file in self.files:
            if file.filename == filename and file.owner == user.username:
                try:
                    with open(file.encrypted_data, "rb") as f:
                        encrypted = f.read()

                    decrypted = EncryptionManager.decrypt(encrypted)
                    return decrypted.decode(errors="ignore")

                except:
                    return ""

        return ""

    # ---------------- EDIT ----------------
    def edit_file(self, user, filename, new_content):
        for file in self.files:
            if file.filename == filename and file.owner == user.username:

                if isinstance(new_content, str):
                    new_content = new_content.encode()

                encrypted = EncryptionManager.encrypt(new_content)

                with open(file.encrypted_data, "wb") as f:
                    f.write(encrypted)

                print("✅ File updated successfully")
                AuditLogger.log(user, "EDIT", filename)
                return True

        print("❌ File not found")
        return False

    # ---------------- LIST ----------------
    def list_files(self, user):
        print("\n📂 Your Files:")
        found = False

        for file in self.files:
            if file.owner == user.username:
                print(f"- {file.filename}")
                found = True

        if not found:
            print("No files found.")

    # ---------------- LOAD ----------------
    def load_files_from_storage(self):
        data = StorageManager.load_files()

        for f in data:
            file_obj = File(
                f["id"],
                f["filename"],
                f["owner"],
                f["path"]
            )

            self.files.append(file_obj)
            self.file_counter = max(self.file_counter, f["id"] + 1)
            file_obj.upload_date = f.get("upload_date", "")

    # ---------------- SAVE ----------------
    def save_files(self):
        data = []

        for file in self.files:
           data.append({
                        "id": file.id,
                        "filename": file.filename,
                        "owner": file.owner,
                        "path": file.encrypted_data,
                        "upload_date": getattr(file, "upload_date", "")
                       })
        StorageManager.save_files(data)

    def delete_file(self, user, filename):
      for file in self.files:
        if file.filename == filename and file.owner == user.username:

            # delete actual file
            if os.path.exists(file.encrypted_data):
                os.remove(file.encrypted_data)

            # remove from list
            self.files.remove(file)

            # update storage
            self.save_files()

            print("🗑 File deleted")
            return True

      return False    