class File:
    def __init__(self, id, filename, owner, encrypted_data):
        self.id = id
        self.filename = filename
        self.owner = owner
        self.encrypted_data = encrypted_data