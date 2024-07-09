class QueueUrlNotSetError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = 'Queue URL is required'


class InvalidWatermarkTypeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = 'Invalid watermark type'