class GenerateUploadUrlError(Exception):
    def __init__(self):
        super().__init__(f"Failed to get upload url.")
