class EnvironmentNotSetError(Exception):
    def __init__(self):
        super().__init__(f"Failed to load environment variables.")
