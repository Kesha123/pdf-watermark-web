class InvalidWatermarkDatatype(Exception):
    def __init__(self):
        super().__init__(f"Invalid watermark data type.")
