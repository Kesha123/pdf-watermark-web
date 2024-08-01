class WatermarkGenerateError(Exception):
    def __init__(self):
        super().__init__(f"Failed to generate watermark.")
