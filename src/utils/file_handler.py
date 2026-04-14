import os

class FileHandler:

    @staticmethod
    def read_file(filepath):
        try:
            with open(filepath, "rb") as f:
                data = f.read()

            filename = os.path.basename(filepath)
            return filename, data

        except FileNotFoundError:
            print("❌ File not found")
            return None, None