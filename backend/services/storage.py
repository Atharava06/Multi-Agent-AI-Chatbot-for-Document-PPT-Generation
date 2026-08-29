class StorageService:
    def save_file(self, content: bytes, path: str):
        with open(path, 'wb') as f:
            f.write(content)
            
    def load_file(self, path: str) -> bytes:
        with open(path, 'rb') as f:
            return f.read()

storage_service = StorageService()
