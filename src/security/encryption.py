class EncryptionManager:

    @staticmethod
    def encrypt(data):
        return bytes([b ^ 0xAA for b in data])   # XOR encryption

    @staticmethod
    def decrypt(data):
        return bytes([b ^ 0xAA for b in data])